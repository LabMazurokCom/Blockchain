<!DOCTYPE html>
<html lang="en">
  <head>
    <script src="https://www.gstatic.com/firebasejs/4.13.0/firebase.js">
    </script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js">
    </script>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="manifest" href="./img/favicons/manifest.json"/>
    <link rel="mask-icon" href="./img/favicons/safari-pinned-tab.svg" color="#5bbad5"/>
    <link rel="shortcut icon" href="./img/favicons/favicon.ico"/>
    <meta name="msapplication-config" content="./img/favicons/browserconfig.xml"/>
    <meta name="theme-color" content="#ffffff"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <meta name="google" content="notranslate"/>
    <meta http-equiv="Content-Language" content="en"/>
    <meta name="description" content="Arbitrage opportunities for trading cryptocurrencies by buying at one exchange and selling on another" />
    <link rel="stylesheet" type="text/css" href="./css/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="./css/jquery.dataTables.min.css"/>
    <link rel="stylesheet" type="text/css" href="./css/jquery-ui.min.css"/>
    <link rel="stylesheet" type="text/css" href="./css/informers.css">
      <link rel="stylesheet" type="text/css" href="./css/denisStyles.css"/>
      <!-- <link rel="stylesheet" type="text/css" href="css/nv.d3.min.css" />		 -->
      <link rel="stylesheet" type="text/css" href="./css/responsive.css" />
      <link rel="stylesheet" type="text/css" href="./css/styles.css" />
      <!-- <link rel="stylesheet" type="text/css" href="css/form2.css" />		 -->
      <link rel="stylesheet" href="./css/font-awesome.min.css"/>
      <link rel="stylesheet" href="./css/hidden_panel.css"/>
      <!-- <script type="text/javascript" src="js/smallCharts.js">
    </script> -->
    <script type="text/javascript" src="plot_spred.js">
    </script>
  </head>
  <body onload = 'setInterval(meta_update, 1000)'>
    <select id = 'currencies'>
      <option value="BTC/USD">BTC/USD</option>
      <option value="ETH/USD">ETH/USD</option>
      <option value="ETH/BTC">ETH/BTC</option>
    </select>
    <select id = "exchange">
      <option value="bitfinex">bitfinex</option>
      <option value="bitstamp">bitstamp</option>
      <option value="cex">cex</option>
      <option value="exmo">exmo</option>
      <option value="gdax">gdax</option>
      <option value="kraken">kraken</option>
      <option value="binance">binance</option>
      <option value="kucoin">kucoin</option>
      <option value="bittrex">bittrex</option>
    </select>

    <select id = 'type'>
      <option value="histogram">histogram</option>
      <option value="scatter">timeseries</option>
    </select>
    <input type="text" id = "number_of_items" value="100">
    <input type="submit" onclick='update()'>
    <input type="checkbox" id = 'fixed_checkbox'>
    <label for="fixed_checkbox"> Fixed Graph</label>
    <div id = 'plot' >

    </div>

  </body>
</html>
