let TEMPLATE = "";
let TEMPLATE_ERR = "";
let templates = {};
let constants = {};
let address = [];
let currency = [];
let CRIPTO_CURRENCIES = [];

function readFromServer(url, callback) {
  return new Promise(function(resolve, reject) {
    var xhr = new XMLHttpRequest();

    let method = 'GET';
    xhr.open(method, url);
    xhr.onload = function() {
      if (this.status >= 200 && this.status < 300) {
        resolve(xhr.responseText);
      } else {
        reject({
          status: this.status,
          statusText: xhr.statusText
        });
      }
    };
    xhr.onerror = function() {
      reject({
        status: this.status,
        statusText: xhr.statusText
      });
    };
    xhr.send();
  }).then((data) => {
    callback(data);
  });
}

// function readFromServer(address, callback) {
//
//   function reqListener() {
//     callback(this.responseText);
//   }
//
//   let xhr = new XMLHttpRequest();
//   xhr.addEventListener('load', reqListener);
//   xhr.open('GET', address);
//   xhr.send();
// }

// readFromServer('js/template.json', function(text) {
//   console.log(text);
//   templates = JSON.parse(text);
//   console.log(templates);
//   TEMPLATE = templates.TEMPLATE.join('\n');
//   TEMPLATE_ERR = templates.TEMPLATE_ERR.join('\n');
//   console.log(TEMPLATE_ERR);
// }).then(() => {
//   console.log("TOLIAAA");
// })

function init() {

  Promise.all(
      [
        readFromServer('js/template.json', function(text) {
          console.log(text);
          templates = JSON.parse(text);
          console.log(templates);
          TEMPLATE = templates.TEMPLATE.join('\n');
          TEMPLATE_ERR = templates.TEMPLATE_ERR.join('\n');
          console.log(TEMPLATE_ERR);
        }),

        readFromServer('js/constants.json', function(text) {
          console.log(text);
          constants = JSON.parse(text);
          console.log(constants);
          address = constants.address;
          currency = constants.currencies;
          CRIPTO_CURRENCIES = constants.cripto_currencies;
        })
      ]
    )
    .then((data) => {
      console.log(data);
    })
    .then(update, error => console.log(error))
    .catch(error => console.log(error));
}


function fixedStateUpdate() {
  try {
    readFromServer('js/order-books.php', function(text) {
      console.log(text);
      let data = text.split('<br></br>')
        .map(x => {
          if (x.length > 2) return x.slice(1, x.length - 1)
          else return ""
        });
      console.log(data);
      for (let i = 0; i < data.length; i++) {
        try {
          data[i] = JSON.parse(data[i]);
        } catch (e) {
          console.log('shit happens')
        }
        showTicker(i, currency[i], data[i]);
      }
    });
  } catch (e) {
    console.log(e);
  }
}


function update_one_pair(id_num) {
  console.log("update_one_pair", id_num, currency);

  let symbol = currency[id_num][0].toLowerCase() + '_' + currency[id_num][1].toLowerCase();

  let firstCall = readFromServer("call_python.php?symbol=" + symbol,
    function(text) {
      console.log(text);
    }
  );

  let secondCall = function() {
    readFromServer(symbol + ".json",
      function(text) {
        let data = JSON.parse(text);
        showTicker(id_num, currency[id_num], data[symbol]);
        console.log(data, symbol);
      }
    )
  }

  firstCall.then(secondCall, secondCall);
}


function update() {

  try {
    console.log("i am in update");
    let flag = false;
    readFromServer("call_python.php", function(text) {
      flag = true;
    });

    for (let i = 0; i < currency.length; i++) {

      let symbol = currency[i][0].toLowerCase() + '_' + currency[i][1].toLowerCase();
      console.log(symbol);

      readFromServer(symbol + ".json", function(text) {
        let data = JSON.parse(text);
        console.log(data, symbol);
        showTicker(i, currency[i], data[symbol]);
      });
    }
  } catch (e) {
    console.log(e);
  }

}

function showTicker(id, currency, data) {

  let maxBid = 0;
  let minAsk = 29 * 1e13;
  let maxBidExchange = "";
  let minAskExchange = "";

  for (let i = 0; i < data["ticker"].length; i++) {
    if (maxBid < data["ticker"][i]["bid"]) {
      maxBid = +data["ticker"][i]["bid"];
      maxBidExchange = data["ticker"][i]["exchange"];
    }

    if (minAsk > data["ticker"][i]["ask"] && data["ticker"][i]["ask"] > 0) {
      minAsk = +data["ticker"][i]["ask"];
      minAskExchange = data["ticker"][i]["exchange"];
    }
  }

  let currentTime = new Date();
  currentTime = currentTime.toString().split(' ')[4];

  maxBid = fixMode(currency[1], maxBid);
  minAsk = fixMode(currency[1], minAsk);

  let percent = ((maxBid - minAsk) / maxBid * 100).toFixed(2);
  let volume = fixMode(currency[1], data['optimal_point']['amount']);
  let profit = fixMode(currency[1], data['optimal_point']['profit']);

  if (profit < 0.001) {
    console.log("There is no arbitrage");
    let resObj = {
      'id': id,
      'currency.first': currency[0],
      'currency.second': currency[1]
    };

    let exch = document.getElementById('exch' + id);
    exch.innerHTML = genTable(TEMPLATE_ERR, resObj);
    console.log(exch.innerHTML);
    console.log("i am here");

    return;
  }

  let askOrders = "";
  let bidOrders = "";

  let n = Object.keys(data["orders"]["asks"]).length;
  let i = 0;

  for (let exch in data["orders"]["asks"]) {
    askOrders += "Buy " +
      fixMode(currency[0], +data["orders"]["asks"][exch][1]) + ' ' +
      currency[0] + " for a price of " +
      fixMode(currency[1], +data["orders"]["asks"][exch][0]) + ' ' +
      currency[1] + " at " + exch;

    if (i < n - 1) askOrders += "<br>";
    i++;
  }

  n = Object.keys(data["orders"]["bids"]).length;
  i = 0;

  for (let exch in data["orders"]["bids"]) {
    bidOrders += "Sell " +
      fixMode(currency[0], +data["orders"]["bids"][exch][1]) + ' ' +
      currency[0] + " for a price of " +
      fixMode(currency[1], +data["orders"]["bids"][exch][0]) + ' ' +
      currency[1] + " at " + exch;

    if (i < n - 1) bidOrders += "<br>";
    i++;
  }

  let resObj = {
    'id': id,
    'currentTime': currentTime,
    'maxBid': maxBid,
    'minAsk': minAsk,
    'percent': percent,
    'volume': volume,
    'profit': profit,
    'askOrders': askOrders,
    'bidOrders': bidOrders,
    'currency.first': currency[0],
    'currency.second': currency[1]
  };

  //Ploting
  let plot = document.createElement('div');

  x = data["amount_points"];
  y = data["profit_points"];
  let plottingData = [{
    x: x,
    y: y,
    type: "scatter",
    mode: "lines+markers",
  }, {
    x: [data.optimal_point.amount],
    y: [data.optimal_point.profit],
    type: "scatter",
    marker: {
      color: "red",
      size: 10
    }
  }];
  let layout = {
    margin: {
      l: 50,
      b: 50,
      t: 5,
      r: 20
    },
    title: false,
    width: 300,
    height: 300,
    xaxis: {
      title: "Amount, " + currency[1],
      titlefont: {
        size: 10
      },
      tickfont: {
        size: 10
      }
    },
    yaxis: {
      title: "Profit, " + currency[1],
      titlefont: {
        size: 10
      },
      tickfont: {
        size: 10
      }
    },
    showlegend: false
  };

  Plotly.plot(plot, plottingData, layout).then(
    function(gd) {
      return Plotly.toImage(gd, {
        format: "svg",
        height: 200,
        width: 300
      }).then(
        function(url) {
          let mainTable = document.getElementById('exch' + id);
          mainTable.innerHTML = genTable(TEMPLATE, resObj);

          console.log(mainTable.innerHTML);
          let img_jpg = document.getElementById("jpg-export" + id);
          img_jpg.src = url;
        }
      )
    });
}

function genTable(template, obj) {
  return formatObj(template, obj);
}

function formatObj(str, dict) {
  let res = str.slice();
  console.log("i am in format");
  for (let key in dict) {
    res = res.replace(new RegExp('(\\{' + key + '\\})', 'g'), dict[key]);
  }
  return res;
}

function fixMode(currency, value) {
  if (CRIPTO_CURRENCIES.indexOf(currency) != -1) {
    return value.toFixed(8);
  }
  return value.toFixed(2);
}
