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
		<!-- <script type="text/javascript" src="js/smallCharts.js"></script> -->

		<script type="text/javascript">

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
			percent = ((maxbid-minask) / maxbid * 100).toFixed(2)
			console.log(maxbid, minask, percent);
			console.log(document.getElementById('max_bid').innerHTML)
			document.getElementById('max_bid').innerHTML = maxbid;
			document.getElementById('min_ask').innerHTML = minask;
			document.getElementById('percent').innerHTML = percent;
			document.getElementById('volume').innerHTML = data['amount'];

			document.getElementById('time').innerHTML = new Date().toString();

			var ask_orders = '';
			var bid_orders = '';
			console.log(data['orders']);
			for(var exch in data['orders']['asks']) {
				ask_orders += 'Buy ' + (+data['orders']['asks'][exch][1]).toFixed(8) + ' BTC for a price of ' + (+data['orders']['asks'][exch][0]).toFixed(2) + ' USD at ' + exch + '<br>';
			}

			for(var exch in data['orders']['bids']) {
				bid_orders += 'Cell ' + (+data['orders']['bids'][exch][1]).toFixed(8) + ' BTC for a price of ' + (+data['orders']['bids'][exch][0]).toFixed(2) + ' USD at ' + exch + '<br>';
			}

			document.getElementById('ask_col_p').innerHTML = ask_orders;
			document.getElementById('bid_col_p').innerHTML = bid_orders;

			document.getElementById('profit').innerHTML = data['profit'];

		}

		function update() {
			file = 'example.json'
			readTextFile(file, function(text){

					var data = JSON.parse(text);
					console.log(data);
					showticker(data);

			});
		}
		</script>


	</head>
	<body onload = 'update();'>






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


<div class = "container">
	<div class="arbitrage-row">
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
								<div class="arbitrage-price" id = 'max_bid'>7682.00000000 EUR</div>
							</div>
							<div class="col-md-3">
								<h4 class="arbitrage-head">Lowest ask price</h4>
								<div class="arbitrage-price" id = 'min_ask'>7307.60000000 EUR</div>
							</div>
							<div class="col-md-3">
								<h4 class="arbitrage-head"> Percentage </h4>
								<div class="arbitrage-price" id = 'percent'>374.40000000 EUR</div>
							</div>
							<div class="col-md-3">
								<h4 class="arbitrage-head">Maximum volume</h4>
								<div class="arbitrage-price" id = 'volume'>0.0006 BTC</div>
							</div>
						</div>
					</div>

				</div>
			</div>
		</div>

		<table style = 'width:100%'>
			<tr>
				<td id = 'ask_col' style = 'width:50%' class="arbitrage-info-text alert">
					<p id = 'ask_col_p' style = 'text-align:left'>

					</p>
				</td>
				<td id = 'bids_col' style = 'width:50%;background-color:#ffe1e6' class="arbitrage-info-text alert">
					<p id = 'bid_col_p' style = 'text-align:left'>

					</p>
				</td>
			</tr>

		</table>

		<div > Your profit will be <span id = 'profit'> </span> </div>
</div>

	</body>
</html>
