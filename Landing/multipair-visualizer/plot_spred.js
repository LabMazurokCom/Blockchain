var flag_was_submit = false;


function plot_graph_spred(currency, exchange, graph_type, data) {
  let n = Object.keys(data).length;
  let spred = [];
  let t = []
  for (let key in data) {
    for (let i = 0; i < data[key]['ticker'].length; i++) {
      if (data[key]['ticker'][i]['exchange'] === exchange &&
        data[key]['ticker'][i]['bid'] != 0) {
        spred.push(parseFloat(data[key]['ticker'][i]['ask']) -
          parseFloat(data[key]['ticker'][i]['bid']));
        t.push(new Date(parseInt(key)));
      }
    }
  }
  let value = spred;
  let key = t;

  if (graph_type == 'histogram') {
    let d = {};
    for (let i = 0; i < spred.length; i++) {
      d[spred[i]] += 1;
    }
    key = Object.keys(d);
    value = [];
    for (let i = 0; i < key.length; i++) {
      value.push(d[key[i]]);
    }

  }
  //Ploting

  data = [{
    x: key,
    y: value,
    type: graph_type,
    mode: "lines+markers",
    marker: {
      color: 'blue',
      size: 5
    }
  }];
  layout = {
    title: false,
    autosize: true,
    // width: 800,
    // height: 800,
    xaxis: {
      title: (graph_type == 'histogram' ? "Spred, " + currency : "Time, sec"),
      titlefont: {
        size: 10
      },
      tickfont: {
        size: 10
      }
    },
    yaxis: {
      title: "Value, " + (graph_type == 'histogram' ? "" : currency),
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
  let type = document.getElementById('type').value;

  begin_address = 'https://arb-log.firebaseio.com/log_'
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
      plot_graph_spred(currencies.split('/')[1], exchange, type, data);
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
