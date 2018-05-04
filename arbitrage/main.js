function readFromServer(address, callback) {

  function reqListener() {
    callback(this.responseText);
  }
  var xhr = new XMLHttpRequest();
  xhr.addEventListener('load', reqListener);
  xhr.open('GET',
    'https://arbitrage-logger.firebaseio.com/log_btc_usd.json?orderBy=%22$key%22&limitToLast=1&print=pretty'
  );
  xhr.send();
}

function readTextFile(file, callback) {
  var result = null;
  var rawFile = new XMLHttpRequest();
  rawFile.overrideMimeType("application/json");
  rawFile.onreadystatechange = function() {
    if (rawFile.readyState === 4 && rawFile.status == "200") {
      callback(rawFile.responseText);
    }
  }
  rawFile.open("GET", file, true);

  rawFile.send(null);
}



function showticker(data) {
  var maxbid = 0;
  var minask = 29 * 1e13;
  var max_bid_exchange = '';
  var min_ask_exchange = '';
  console.log(data['ticker'])

  for (var i = 0; i < data['ticker'].length; i++) {
    if (maxbid < data['ticker'][i]['bid']) {
      maxbid = +data['ticker'][i]['bid'];
      max_bid_exchange = data['ticker'][i]['exchange'];
    }
    if (minask > data['ticker'][i]['ask']) {
      minask = +data['ticker'][i]['ask'];
      min_ask_exchange = data['ticker'][i]['exchange'];
    }
  }

  maxbid = maxbid.toFixed(2);
  minask = minask.toFixed(2);
  percent = ((maxbid - minask) / maxbid * 100).toFixed(2)

  console.log(maxbid, minask, percent);
  console.log(document.getElementById('max_bid').innerHTML)

  document.getElementById('max_bid').innerHTML = maxbid;
  document.getElementById('min_ask').innerHTML = minask;
  document.getElementById('percent').innerHTML = percent;
  document.getElementById('volume').innerHTML = data['amount'].toFixed(2);

  document.getElementById('time').innerHTML = new Date().toString();

  var ask_orders = '';
  var bid_orders = '';
  console.log(data['orders']);
  var n = Object.keys(data['orders']['asks']).length;
  var i = 0;
  for (var exch in data['orders']['asks']) {
    ask_orders += 'Buy ' + (+data['orders']['asks'][exch][1]).toFixed(8) +
      ' BTC for a price of ' + (+data['orders']['asks'][exch][0]).toFixed(2) +
      ' USD at ' + exch;

    if (i < n - 1) ask_orders += '<br>';
    i++;
  }
  var n = Object.keys(data['orders']['bids']).length;
  var i = 0;
  for (var exch in data['orders']['bids']) {
    bid_orders += 'Sell ' + (+data['orders']['bids'][exch][1]).toFixed(8) +
      ' BTC for a price of ' + (+data['orders']['bids'][exch][0]).toFixed(2) +
      ' USD at ' + exch;
    if (i < n - 1) bid_orders += '<br>';
    i++;
  }

  console.log(ask_orders);
  console.log(bid_orders);



  document.getElementById('ask_col_p').innerHTML = ask_orders;
  document.getElementById('bid_col_p').innerHTML = bid_orders;

  let table0 = document.getElementById('table0');
  let table1 = document.getElementById('table1');
  console.log(table0, table1);
  table1.style.width = table0.style.width;

  document.getElementById('profit').innerHTML = data['profit'].toFixed(2);

  // var ask_col = document.getElementById('ask_col');
  // var bid_col = document.getElementById('bid_col');

  //
  //Ploting
  var d3 = Plotly.d3;
  var img_jpg = d3.select('#jpg-export');

  var myPlot = document.getElementById('plot');
  x = data['amount_points'];
  y = data['profit_points'];
  // console.log(x);
  // console.log('\n\n\n')
  // console.log(y);
  // console.log(data.optimal_point)
  data = [{
    x: x,
    y: y,
    type: 'scatter',
    mode: 'lines+markers',
  }, {
    x: [data.optimal_point.amount],
    y: [data.optimal_point.profit],
    type: 'scatter',
    marker: {
      color: 'red',
      size: 10
    }
  }];
  layout = {
    // title: 'Profit vs Amount',
    // titlefont:{
    // 	size:14
    // },
    // autosize: true,
    // autoscale: true,
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
      title: 'Amount, USD',
      titlefont: {
        size: 10
      },
      tickfont: {
        size: 7
      }
    },
    yaxis: {
      title: 'Profit, USD',
      titlefont: {
        size: 10
      },
      tickfont: {
        size: 7
      }
    },
    showlegend: false
  };
  /*
								var trace = {
					x: response_json.amount_points,
					y: response_json.profit_points,
					mode: 'lines+markers'
				};
				var data = [trace];
				var layout = {
					title: 'Profit to Amount',
					autosize: false,
					width: 800,
					height: 500,
					xaxis: {title: 'Amount, USD'},
					yaxis: {title: 'Profit, USD'}
				};
				*/
  try {
    Plotly.deleteTraces(plot, [-2, -1]);
  } catch (e) {}
  Plotly.plot('plot', data, layout).then(
    function(gd) {
      return Plotly.toImage(gd, {
        format: 'svg',
        height: 150,
        width: 300
      }).then(
        function(url) {
          img_jpg.attr("src", url);
        }
      )
    });

}

function showticker1(data) {
  var maxbid = 0;
  var minask = 29 * 1e13;
  var max_bid_exchange = '';
  var min_ask_exchange = '';
  console.log(data['ticker'])

  for (var i = 0; i < data['ticker'].length; i++) {
    if (maxbid < data['ticker'][i]['bid']) {
      maxbid = +data['ticker'][i]['bid'];
      max_bid_exchange = data['ticker'][i]['exchange'];
    }
    if (minask > data['ticker'][i]['ask']) {
      minask = +data['ticker'][i]['ask'];
      min_ask_exchange = data['ticker'][i]['exchange'];
    }
  }

  maxbid = maxbid.toFixed(2);
  minask = minask.toFixed(2);
  percent = ((maxbid - minask) / maxbid * 100).toFixed(2)

  console.log(maxbid, minask, percent);
  console.log(document.getElementById('max_bid1').innerHTML)

  document.getElementById('max_bid1').innerHTML = maxbid;
  document.getElementById('min_ask1').innerHTML = minask;
  document.getElementById('percent1').innerHTML = percent;
  document.getElementById('volume1').innerHTML = data['amount'].toFixed(2);

  document.getElementById('time1').innerHTML = new Date().toString();

  var ask_orders = '';
  var bid_orders = '';
  console.log(data['orders']);
  var n = Object.keys(data['orders']['asks']).length;
  var i = 0;
  for (var exch in data['orders']['asks']) {
    ask_orders += 'Buy ' + (+data['orders']['asks'][exch][1]).toFixed(8) +
      ' BTC for a price of ' + (+data['orders']['asks'][exch][0]).toFixed(2) +
      ' USD at ' + exch;

    if (i < n - 1) ask_orders += '<br>';
    i++;
  }
  var n = Object.keys(data['orders']['bids']).length;
  var i = 0;
  for (var exch in data['orders']['bids']) {
    bid_orders += 'Sell ' + (+data['orders']['bids'][exch][1]).toFixed(8) +
      ' BTC for a price of ' + (+data['orders']['bids'][exch][0]).toFixed(2) +
      ' USD at ' + exch;
    if (i < n - 1) bid_orders += '<br>';
    i++;
  }

  console.log(ask_orders);
  console.log(bid_orders);

  document.getElementById('ask_col_p1').innerHTML = ask_orders;
  document.getElementById('bid_col_p1').innerHTML = bid_orders;

  document.getElementById('profit1').innerHTML = data['profit'].toFixed(2);

  var ask_col = document.getElementById('ask_col1');
  var bid_col = document.getElementById('bid_col1');
  console.log(ask_col, bid_col);

  //
  //Ploting
  var d3 = Plotly.d3;
  var img_jpg = d3.select('#jpg-export1');

  var myPlot = document.getElementById('plot');
  x = data['amount_points'];
  y = data['profit_points'];
  // console.log(x);
  // console.log('\n\n\n')
  // console.log(y);
  // console.log(data.optimal_point)
  data = [{
    x: x,
    y: y,
    type: 'scatter',
    mode: 'lines+markers',
  }, {
    x: [data.optimal_point.amount],
    y: [data.optimal_point.profit],
    type: 'scatter',
    marker: {
      color: 'red',
      size: 10
    }
  }];
  layout = {
    // title: 'Profit vs Amount',
    // titlefont:{
    // 	size:14
    // },
    // autosize: true,
    // autoscale: true,
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
      title: 'Amount, USD',
      titlefont: {
        size: 10
      },
      tickfont: {
        size: 7
      }
    },
    yaxis: {
      title: 'Profit, USD',
      titlefont: {
        size: 10
      },
      tickfont: {
        size: 7
      }
    },
    showlegend: false
  };
  /*
								var trace = {
					x: response_json.amount_points,
					y: response_json.profit_points,
					mode: 'lines+markers'
				};
				var data = [trace];
				var layout = {
					title: 'Profit to Amount',
					autosize: false,
					width: 800,
					height: 500,
					xaxis: {title: 'Amount, USD'},
					yaxis: {title: 'Profit, USD'}
				};
				*/
  try {
    Plotly.deleteTraces(plot, [-2, -1]);
  } catch (e) {}
  Plotly.plot('plot', data, layout).then(
    function(gd) {
      return Plotly.toImage(gd, {
        format: 'svg',
        height: 150,
        width: 300
      }).then(
        function(url) {
          console.log('url is ', url);
          img_jpg.attr("src", url);
        }
      )
    });

}

function update() {
  file = './read_from_firebase.php';
  address =
    'https://arbitrage-logger.firebaseio.com/log_btc_usd.json?orderBy=%22$key%22&limitToLast=1'
  try {
    readFromServer(address, function(text) {

      var data = JSON.parse(text);
      console.log(data);
      showticker(data[Object.keys(data)[0]]);
      showticker1(data[Object.keys(data)[0]]);

    });
  } catch (e) {
    console.log('here we have failed');
  }
}
