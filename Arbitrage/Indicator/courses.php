<h1>BTC-USDT</h1>
<?php 
	$options  = array('http' => array('user_agent' => 'curl/7.29.0'));
	$context  = stream_context_create($options);

	$x = file_get_contents('https://api.binance.com/api/v3/ticker/bookTicker?symbol=BTCUSDT', false, $context); 
	$y = json_decode($x,true); 
	echo "binance", "\n", $y[bidPrice], "\n", $y[askPrice], "\n";
	echo "<br />\n";

	$x = file_get_contents('https://www.bitstamp.net/api/v2/ticker/btcusd', false, $context); 
	$y = json_decode($x,true); 
	echo "binance", "\n", $y[bid], "\n", $y[ask], "\n";
	echo "<br />\n";

	$x = file_get_contents('https://cex.io/api/ticker/BTC/USD', false, $context); 
	$y = json_decode($x,true); 
	echo "cex", "\n", $y[bid], "\n", $y[ask], "\n";
	echo "<br />\n";

	$x = file_get_contents('https://api.gdax.com/products/BTC-USD/ticker', false, $context); 
	$y = json_decode($x,true); 
	echo "gdax", "\n", $y[bid], "\n", $y[ask], "\n";
	echo "<br />\n";
/*
	$x = file_get_contents('https://api.hitbtc.com/api/2/public/ticker/BTCUSD', false, $context); 
	$y = json_decode($x,true); 
	echo "hitbtc", "\n", $y[bid], "\n", $y[ask], "\n";
	echo "<br />\n";
*/
	$x = file_get_contents('https://api.kucoin.com/v1/open/tick?symbol=BTC-USDT', false, $context); 
	$y = json_decode($x,true); 
	echo "kucoin", "\n", $y[data][buy], "\n", $y[data][sell], "\n";
	echo "<br />\n";

	$x = file_get_contents('https://api.exmo.com/v1/ticker', false, $context); 
	$y = json_decode($x,true); 
	echo "exmo", "\n", $y[BTC_USDT][buy_price], "\n", $y[BTC_USDT][sell_price];
	echo "<br />\n";
?>
