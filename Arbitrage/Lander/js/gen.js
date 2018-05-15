const template =
  `
    <ul class="list-unstyled pricing-table active text-center">
      <li class="headline"><h5 class="white">{currency.first}/{currency.second}</h5></li>
      <li class="price"><div class="amount">{profit} {currency.second}</div></li>
      <li class="info"> <img id="jpg-export{id}" style="width:100%"></img></li>
      <li class="features">{ask_orders}</li>
      <li class="features">{bid_orders}</li>
      <li class="features last btn btn-secondary btn-wide"><a href="#">Get Started</a></li>
    </ul>
`

const template_err =
  `
    <ul class="list-unstyled pricing-table active text-center">
      <li class="headline"><h5 class="white">{currency.first}/{currency.second}</h5></li>
      <li class="info">No arbitrage</li>


    </ul>
`

function genTable(obj) {
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

let cripto = [
  'BTC', 'ETH'
];

function fixMode(currency, value) {
  if (cripto.indexOf(currency) != -1) return value.toFixed(8);
  else {
    return value.toFixed(2);
  }
}

function showticker(id, currency, data) {

  var maxbid = 0;
  var minask = 29 * 1e13;
  var max_bid_exchange = "";
  var min_ask_exchange = "";

  for (var i = 0; i < data["ticker"].length; i++) {
    if (maxbid < data["ticker"][i]["bid"]) {
      maxbid = +data["ticker"][i]["bid"];
      max_bid_exchange = data["ticker"][i]["exchange"];
    }
    if (minask > data["ticker"][i]["ask"] && data["ticker"][i]["ask"] > 0) {
      minask = +data["ticker"][i]["ask"];
      min_ask_exchange = data["ticker"][i]["exchange"];
    }
  }

  let cur_time = new Date();
  cur_time = cur_time.toString().split(' ')[4];

  maxbid = fixMode(currency[1], maxbid);
  minask = fixMode(currency[1], minask);
  let percent = ((maxbid - minask) / maxbid * 100).toFixed(2);
  let volume = fixMode(currency[1], data['optimal_point']['amount']);
  let profit = fixMode(currency[1], data['optimal_point']['profit']);
  console.log(profit);
  if (profit === 0) {
    let res_obj = {
      'currency.first': currency[0],
      'currency.second': currency[1]
    };
    document.getElementById('exch' + id).innerHTML = genTable(template_err,
      res_obj);
    return;
  }

  console.log(profit, 'and i am after terminal if')

  var ask_orders = "";
  var bid_orders = "";
  console.log(data["orders"]);
  var n = Object.keys(data["orders"]["asks"]).length;
  var i = 0;

  for (var exch in data["orders"]["asks"]) {
    ask_orders += "Buy " + fixMode(currency[0], +data["orders"]["asks"][exch]
        [1]) +
      ' ' +
      currency[0] + " for a price of " + fixMode(currency[1], +data["orders"]
        [
          "asks"
        ][
          exch
        ][0]) + ' ' +
      currency[1] + " at " + exch;

    if (i < n - 1) ask_orders += "<br>";
    i++;
  }

  var n = Object.keys(data["orders"]["bids"]).length;
  var i = 0;
  for (var exch in data["orders"]["bids"]) {
    bid_orders += "Sell " + fixMode(currency[0], +data["orders"]["bids"][exch]
        [
          1
        ]) + ' ' +
      currency[0] + " for a price of " + fixMode(currency[1], +data["orders"]
        [
          "bids"
        ][
          exch
        ][0]) + ' ' +
      currency[1] + " at " + exch;
    if (i < n - 1) bid_orders += "<br>";
    i++;
  }

  // console.log(ask_orders);
  // console.log(bid_orders);

  //create build vector
  let res_array = [
    id,
    cur_time,
    maxbid,
    minask,
    percent,
    volume,
    profit,
    ask_orders,
    bid_orders,
    currency[0],
    currency[1]
  ];

  let plot = document.createElement('div');
  let res_obj = {
    'id': id,
    'cur_time': cur_time,
    'maxbid': maxbid,
    'minask': minask,
    'percent': percent,
    'volume': volume,
    'profit': profit,
    'ask_orders': ask_orders,
    'bid_orders': bid_orders,
    'currency.first': currency[0],
    'currency.second': currency[1]
  };
  //Ploting

  x = data["amount_points"];
  y = data["profit_points"];
  // console.log(x);
  // console.log("\n\n\n")
  // console.log(y);
  // console.log(data.optimal_point)
  data = [{
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
  layout = {
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

  try {
    Plotly.deleteTraces(plot, [-2, -1]);
  } catch (e) {}
  Plotly.plot(plot, data, layout).then(
    function(gd) {
      return Plotly.toImage(gd, {
        format: "svg",
        height: 200,
        width: 300
      }).then(
        function(url) {
          let mainTable = document.getElementById('exch' + id);
          mainTable.innerHTML = genTable(res_obj);

          console.log(mainTable.innerHTML);
          let img_jpg = document.getElementById("jpg-export" + id);
          img_jpg.src = url;
        }
      )
    });
}

function readFromServer(address, callback) {

  function reqListener() {
    callback(this.responseText);
  }
  var xhr = new XMLHttpRequest();
  xhr.addEventListener('load', reqListener);
  xhr.open('GET', address);
  xhr.send();
}

function update() {

  address = [
    'https://test-logger-96bb2.firebaseio.com/log_btc_usd.json?orderBy=%22$key%22&limitToLast=1',
    'https://test-logger-96bb2.firebaseio.com/log_eth_usd.json?orderBy=%22$key%22&limitToLast=1',
    'https://test-logger-96bb2.firebaseio.com/log_btc_usdt.json?orderBy=%22$key%22&limitToLast=1'
  ];

  currency = [
    ['BTC', 'USD'],
    ['ETH', 'USD'],
    ['BTC', 'USDT']
  ];

  let j = 0;
  for (let i = 0; i < address.length; i++) {
    try {
      readFromServer(address[i], function(text) {
        var data = JSON.parse(text);
        console.log(data);
        showticker(i, currency[i], data[Object.keys(data)[0]]);
      })
    } catch (e) {
      console.log('here we have failed with exchange #' + i);
      console.log(e);
    }
  }

}
