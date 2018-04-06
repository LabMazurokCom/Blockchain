<h1>BTC-USDT</h1>
<h2>binance</h2>
	<?php echo file_get_contents('https://api.binance.com/api/v3/ticker/bookTicker?symbol=BTCUSDT'); ?>
<h2>bitstamp</h2>
	<?php echo file_get_contents('https://www.bitstamp.net/api/v2/ticker/btcusd'); ?>
<h2>cex</h2>
	<?php echo file_get_contents('https://cex.io/api/ticker/BTC/USD'); ?>
<h2>gdax</h2>
	<?php echo file_get_contents('https://api.gdax.com/products/BTC-USD/ticker'); ?>
<h2>hitbtc</h2>
	<?php echo file_get_contents('https://api.hitbtc.com/api/2/public/ticker/BTCUSD'); ?>
<h2>kucoin</h2>
	<?php echo file_get_contents('https://api.kucoin.com/v1/open/tick?symbol=BTC-USDT'); ?>
<h2>exmo</h2>
	<?php echo file_get_contents('https://api.exmo.com/v1/ticker'); ?>
