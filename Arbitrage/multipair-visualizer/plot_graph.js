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

let currencies = 'None'
let exchange = 'None'
let true_num = 'None'
let ok = 'None'

let begin_address = 'https://arb-log.firebaseio.com/log_';
let middle_address = '.json?orderBy=%22$key%22&limitToLast=';
let curr_array = {
  "BTC/USD": 'btc_usd',
  "ETH/USD": 'eth_usd',
  "ETH/BTC": 'eth_btc'
};

let data = {};

function update(currencies, exchange, num) {
  flag_was_submit = true;
  address = begin_address + curr_array[currencies] + middle_address + num;
  console.log(address);
  try {
    readFromServer(address, function(text) {
      data = Object.assign(data, JSON.parse(text));
      let keys = Object.keys(data);
      keys.sort();
      let n = keys.length - true_num;
      for (let i = 0; i < n; i++) {
        delete data[keys[i]];
      }
      console.log(data);
      plot_graph_askbid(currencies.split('/')[1], exchange, data);
    });
  } catch (e) {
    console.log(e);
  }
}

function meta_update() {
  let cur_ok = document.getElementById('fixed_checkbox').checked;
  let cur_currencies = document.getElementById('currencies').value;
  let cur_exchange = document.getElementById('exchange').value;
  let cur_num = parseInt(document.getElementById('number_of_items').value);

  let something_changed = ok != cur_ok |
    currencies != cur_currencies |
    cur_exchange != exchange;

  let set_num = 1;
  if (something_changed) {
    ok = cur_ok;
    currencies = cur_currencies;
    exchange = cur_exchange;
    true_num = cur_num;
    set_num = cur_num;
  } else if (true_num == cur_num) {
    set_num = cur_num;
  } else {
    true_num = cur_num;
    if (true_num > curnum) {
      let keys = Object.keys(data);
      keys.sort();
      let n = true_num - cur_num + 1;
      for (let i = 0; i < n; i++) {
        delete data[keys[i]];
      }
      true_num = cur_num;
      set_num = 1;
    } else {
      set_num = cur_num;
    }

  }
  if (!ok && flag_was_submit) {
    update(currencies, exchange, set_num);
  }
}
