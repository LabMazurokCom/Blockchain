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
		<style media="screen">
			div.container {
				display: inline-block;
			}
			.rectangular {
				-webkit-clip-path: inset(30px 10px 30px 10px);
				clip-path: inset(30px 10px 30px 10px);
			}
		</style>
		<script type="text/javascript" src="main.js"></script>


	</head>
	<body onload = 'update();setInterval(update, 5000);'>

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

		<table>

			<tr>

			<td>
					<!-- table with extra bids and asks -->
				<table id = 'table0'>
					<tr >
						<td colspan="5">
							<div class="panel-heading">
								<div class="table_title container cust_container">
									<div> <span>BTC/USD</span> </div>
									<div> <span id = 'time'></span></div>
								</div>
							</div>
						</td>
					</tr>
					<tr>
						<td style ='width:20%'><h4 class="arbitrage-head">Highest bid price</h4></td>
						<td style ='width:20%'><h4 class="arbitrage-head">Lowest ask price</h4></td>
						<td style ='width:20%'><h4 class="arbitrage-head">Percentage</h4></td>
						<td style ='width:20%'><h4 class="arbitrage-head">Maximum volume</h4></td>
						<td style ='width:20%'><h4 class="arbitrage-head">Profit</h4></td>
					</tr>
					<tr>
						<td style ='width:20%'><div class="arbitrage-price" id = 'max_bid'></div></td>
						<td style ='width:20%'><div class="arbitrage-price" id = 'min_ask'></div></td>
						<td style ='width:20%'><div class="arbitrage-price" id = 'percent'></div></td>
						<td style ='width:20%'><div class="arbitrage-price" id = 'volume'></div></td>
						<td style ='width:20%'><div class="arbitrage-price" id = 'profit'></div></td>

					</tr>`

				</table>
				<table id = 'table1'>
					<tr>
						<td id = 'ask_col' style = 'background-color:#ffe1e6;width:50%' class="arbitrage-info-text alert">
							<p id = 'ask_col_p' style = 'text-align:left;font-size:60%'></p>
						</td>
						<td id = 'bid_col' style = 'width:50%' class="arbitrage-info-text alert">
							<p id = 'bid_col_p' style = 'text-align:left;font-size:60%'> </p>
						</td>
					</tr>
				</table>

					<!-- orders -->

			</td>
			<td>
				<div class="container1" >
					<img id="jpg-export"></img>
				</div>

			</td>
		</tr>
		</table>

		</div>
		<div class="main main-content arbitrage arbitrage-container" style="padding-top: 40px;">

		<table>

			<tr>

			<td>
					<!-- table with extra bids and asks -->
				<table name = 'table1'>
					<tr >
						<td colspan="5">
							<div class="panel-heading">
								<div class="table_title container cust_container">
									<div> <span>BTC/USD</span> </div>
									<div> <span id = 'time1'></span></div>
								</div>
							</div>
						</td>
					</tr>
					<tr>
						<td style ='width:20%'><h4 class="arbitrage-head">Highest bid price</h4></td>
						<td style ='width:20%'><h4 class="arbitrage-head">Lowest ask price</h4></td>
						<td style ='width:20%'><h4 class="arbitrage-head">Percentage</h4></td>
						<td style ='width:20%'><h4 class="arbitrage-head">Maximum volume</h4></td>
						<td style ='width:20%'><h4 class="arbitrage-head">Profit</h4></td>
					</tr>
					<tr>
						<td style ='width:20%'><div class="arbitrage-price" id = 'max_bid1'></div></td>
						<td style ='width:20%'><div class="arbitrage-price" id = 'min_ask1'></div></td>
						<td style ='width:20%'><div class="arbitrage-price" id = 'percent1'></div></td>
						<td style ='width:20%'><div class="arbitrage-price" id = 'volume1'></div></td>
						<td style ='width:20%'><div class="arbitrage-price" id = 'profit1'></div></td>

					</tr>`

				</table>
				<table style.width = table1.style.width>
					<tr>
						<td id = 'ask_col1' style = 'background-color:#ffe1e6;width:50%' class="arbitrage-info-text alert">
							<p id = 'ask_col_p1' style = 'text-align:left;font-size:60%'></p>
						</td>
						<td id = 'bid_col1' style = 'width:50%' class="arbitrage-info-text alert">
							<p id = 'bid_col_p1' style = 'text-align:left;font-size:60%'> </p>
						</td>
					</tr>
				</table>

					<!-- orders -->

			</td>
			<td>
				<div class="container1" >
					<img id="jpg-export1"></img>
				</div>

			</td>
		</tr>
		</table>

		</div>
		<div id = 'plot' style="display:none;"> </div>
</html>
