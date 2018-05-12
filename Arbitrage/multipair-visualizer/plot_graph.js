var flag_was_submit = false;

function plot_graph_askbid(currency, exchange, data) {
  let n = Object.keys(data).length;
  let asks = [];
  let bids = [];
  let t = []
  for (let key in data) {
    for (let i = 0; i < data[key]['ticker'].length; i++) {
      if (data[key]['ticker'][i]['exchange'] === exchange &&
        data[key]['ticker'][i]['bid'] != 0) {
        bids.push(parseFloat(data[key]['ticker'][i]['bid']));
        asks.push(parseFloat(data[key]['ticker'][i]['ask']));
        t.push(new Date(parseInt(key)));
      }
    }
  }

  //Ploting
  data = [{
    x: t,
    y: bids,
    type: "scatter",
    mode: "lines+markers",
    marker: {
      color: 'green',
      size: 5
    }
  }, {
    x: t,
    y: asks,
    type: "scatter",
    mode: "lines+markers",
    marker: {
      color: "red",
      size: 5
    }
  }];
  layout = {
    title: false,
    autosize: true,
    // width: 800,
    // height: 800,
    xaxis: {
      title: "Time, sec",
      titlefont: {
        size: 10
      },
      tickfont: {
        size: 10
      }
    },
    yaxis: {
      title: "Value, " + currency,
      titlefont: {
        size: 10
      },
      tickfont: {
        size: 10
      }
    },
    showlegend: false
  };

  Plotly.newPlot('plot', data, layout);
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
  flag_was_submit = true;
  let currencies = document.getElementById('currencies').value;
  let exchange = document.getElementById('exchange').value;
  let num = parseInt(document.getElementById('number_of_items').value);
  begin_address = 'https://test-logger-96bb2.firebaseio.com/log_'
  middle_address = '.json?orderBy=%22$key%22&limitToLast='
  curr_array = {
    "BTC/USD": 'btc_usd',
    "ETH/USD": 'eth_usd',
    "ETH/BTC": 'eth_btc'
  };

  address = begin_address + curr_array[currencies] + middle_address + num;
  console.log(address);
  try {
    readFromServer(address, function(text) {
      var data = JSON.parse(text);
      console.log(data);
      plot_graph_askbid(currencies.split('/')[1], exchange, data);
    });
  } catch (e) {
    console.log(e);
  }
}

function meta_update() {
  let ok = document.getElementById('fixed_checkbox').checked;
  if (!ok && flag_was_submit) {
    update();
  }
}
