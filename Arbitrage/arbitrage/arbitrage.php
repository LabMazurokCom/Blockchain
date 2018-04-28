<!DOCTYPE html>
<html lang="en">
	<head>
		<title>Arbitrage opportunities</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<link rel="apple-touch-icon" sizes="180x180" href="./img/favicons/apple-touch-icon.png">
		<link rel="icon" type="image/png" sizes="32x32" href="./img/favicons/favicon-32x32.png">
		<link rel="icon" type="image/png" sizes="16x16" href="./img/favicons/favicon-16x16.png">
		<link rel="manifest" href="./img/favicons/manifest.json">
		<link rel="mask-icon" href="./img/favicons/safari-pinned-tab.svg" color="#5bbad5">
		<link rel="shortcut icon" href="./img/favicons/favicon.ico">
				<meta name="msapplication-config" content="./img/favicons/browserconfig.xml">
		<meta name="theme-color" content="#ffffff">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<meta name="google" content="notranslate">
		<meta http-equiv="Content-Language" content="en">
		<meta name="description" content="Arbitrage opportunities for trading cryptocurrencies by buying at one exchange and selling on another" />
		<link rel="stylesheet" type="text/css" href="./css/bootstrap.min.css" />
		<link rel="stylesheet" type="text/css" href="./css/jquery.dataTables.min.css">
		<link rel="stylesheet" type="text/css" href="./css/jquery-ui.min.css">
		<!-- <link rel="stylesheet" type="text/css" href="css/nv.d3.min.css" />		 -->
		<link rel="stylesheet" type="text/css" href="./css/responsive.css" />
    	<link rel="stylesheet" type="text/css" href="./css/styles.css" />
		    	<!-- <link rel="stylesheet" type="text/css" href="css/form2.css" />		 -->
		<link rel="stylesheet" href="./css/font-awesome.min.css">
		<link href="/css/fonts.googleapis.com.montserrat.100.900.css" rel="stylesheet">
						    	<script type="text/javascript" src="./js/jquery.min.js"></script>
		<script type="text/javascript" src="./js/jquery-ui.min.js"></script>
		<script type="text/javascript" src="./js/popper.min.js"></script>
        <script src="./js/bootstrap.min.js"></script>
		<script src="./js/jquery.dataTables.1.10.16.min.js"></script>
		<script type="text/javascript" src="./js/main.js"></script>
		<script type="text/javascript" src="./js/main-search.js"></script>
		<script src="https://www.gstatic.com/firebasejs/4.13.0/firebase.js"></script>
		<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
		<!-- <script type="text/javascript" src="js/smallCharts.js"></script> -->

		<script type="text/javascript">

		function readFromServer(address, callback) {

			function reqListener () {
				callback(this.responseText);
			}
			var xhr = new XMLHttpRequest();
			xhr.addEventListener('load', reqListener);
			xhr.open('GET', 'https://arbitrage-logger.firebaseio.com/log_btc_usd.json?orderBy=%22$key%22&limitToLast=1&print=pretty');
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
			for(var i = 0 ; i < data['ticker'].length; i++) {
				if(maxbid < data['ticker'][i]['bid']) {
					maxbid = +data['ticker'][i]['bid'];
					max_bid_exchange = data['ticker'][i]['exchange'];
				}
				if(minask > data['ticker'][i]['ask']) {
					minask = +data['ticker'][i]['ask'];
					min_ask_exchange = data['ticker'][i]['exchange'];
				}
			}
			maxbid = maxbid.toFixed(2);
			minask = minask.toFixed(2);
			percent = ((maxbid-minask) / maxbid * 100).toFixed(2)
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
			for(var exch in data['orders']['asks']) {
				ask_orders += 'Buy ' + (+data['orders']['asks'][exch][1]).toFixed(8) + ' BTC for a price of ' + (+data['orders']['asks'][exch][0]).toFixed(2) + ' USD at ' + exch;

				if(i < n - 1) ask_orders += '<br>';
				i++;
			}
			var n = Object.keys(data['orders']['bids']).length;
			var i = 0;
			for(var exch in data['orders']['bids']) {
				bid_orders += 'Sell ' + (+data['orders']['bids'][exch][1]).toFixed(8) + ' BTC for a price of ' + (+data['orders']['bids'][exch][0]).toFixed(2) + ' USD at ' + exch;
				if(i < n - 1) bid_orders += '<br>';
				i++;
			}

			console.log(ask_orders);
			console.log(bid_orders);

			document.getElementById('ask_col_p').innerHTML = ask_orders;
			document.getElementById('bid_col_p').innerHTML = bid_orders;

			document.getElementById('profit').innerHTML = data['profit'].toFixed(2);

			var ask_col = document.getElementById('ask_col');
			var bid_col = document.getElementById('bid_col');
			console.log(ask_col, bid_col);

			//
			//Ploting
			var myPlot = document.getElementById('plot');
			x = data['amount_points'];
			y = data['profit_points'];
			console.log(x);
			console.log('\n\n\n')
			console.log(y);
			console.log(data.optimal_point)
			data = [
				{x: x,
				 y: y,
				 type: 'scatter',
				 mode: 'lines+markers',
				},
				{x: [data.optimal_point.amount],
				 y: [data.optimal_point.profit],
				 type: 'scatter',
				 marker: {color: 'red', size: 10}
				}
			];
			layout = {
				title: 'Profit vs Amount',
				autosize: true,
				autoscale: true,
				// width: 800,
				// height: 500,
				xaxis: {title: 'Amount, USD'},
				yaxis: {title: 'Profit, USD'},
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
				Plotly.newPlot('plot', data, layout);
				myPlot.on('plotly_click', function(){
						alert('LIST OF ORDERS WILL BE FORMED HERE');
				});

		}

		function update() {
			file = './read_from_firebase.php';
			address = 'https://arbitrage-logger.firebaseio.com/log_btc_usd.json?orderBy=%22$key%22&limitToLast=1'
			try {
				readFromServer(address, function(text){

						var data = JSON.parse(text);
						console.log(data);
						showticker(data[Object.keys(data)[0]]);

				});
			}
			catch(e) {
				console.log('here we have failed');
			}
		}


		</script>


	</head>
	<body onload = 'setInterval(update, 5000);'>

		<div class="main main-content arbitrage arbitrage-container" style="padding-top: 40px;">
			<div class="container cust_container">
				<div class="row">
			    	<div class="col-12">
			          <h4 class="title">Arbitrage Opportunities for Cryptocurrencies</h4>
			            <p class="text">
							There are many different markets for the wide variety of crypto-coins. Any given asset (coin) will be offered at different prices across these markets.
							Clear opportunities for <a href="https://en.wikipedia.org/wiki/Arbitrage" target="_blank">Arbitrage</a> ( taking advantage of a price difference between markets ). This page will you show you the best opportunities for doing such trades.
						</p>
			    	</div>
		    	</div>
			</div>


<div class = "container234"  >
	<div class="arbitrage-row" style = 'width:50%'>
			<div class="panel-heading">
				<div class="table_title container cust_container">
					<div> <span>BTC/USD</span> </div>
					<div> <span id = 'time'></span></div>
				</div>
			</div>
			<div class="container cust_container">
				<div class="panel panel-default">
					<div class="panel-body">
						<div class="row">
							<div class="col-md-3">
								<h4 class="arbitrage-head">Highest bid price</h4>
								<div class="arbitrage-price" id = 'max_bid'></div>
							</div>
							<div class="col-md-3">
								<h4 class="arbitrage-head">Lowest ask price</h4>
								<div class="arbitrage-price" id = 'min_ask'></div>
							</div>
							<div class="col-md-3">
								<h4 class="arbitrage-head"> Percentage </h4>
								<div class="arbitrage-price" id = 'percent'></div>
							</div>
							<div class="col-md-3">
								<h4 class="arbitrage-head">Maximum volume</h4>
								<div class="arbitrage-price" id = 'volume'></div>
							</div>
						</div>
					</div>

				</div>
			</div>
		</div>

		<table style = 'width:50%'>
			<tr>
				<td id = 'ask_col' style = 'width:50%;background-color:#ffe1e6' class="arbitrage-info-text alert">
					<p id = 'ask_col_p' style = 'text-align:left;font-size:60%'>

					</p>
				</td>
				<td id = 'bid_col' style = 'width:50%' class="arbitrage-info-text alert">
					<p id = 'bid_col_p' style = 'text-align:left;font-size:60%'>

					</p>
				</td>
			</tr>

		</table>

		<div class="panel-heading">
			<div class="table_title container cust_container">
				<p class="text">
						Your profit will be <span id = 'profit'> </span> USD
				</p>
			</div>
		</div>
		<div id = 'plot' style = 'width:50%; padding-left:50%; padding-top:0%' >
		</div>

</html>
