<?php
	// JSON array of (bourse, bid, ask)
	$options  = array('http' => array('user_agent' => 'curl/7.29.0'));
	$context  = stream_context_create($options);
	echo '{ "list": [';
	$x = file_get_contents('https://api.binance.com/api/v3/ticker/bookTicker?symbol=BTCUSDT', false, $context); 
	$y = json_decode($x,true); 
	echo '{"exchange":"binance", "bid":', $y[bidPrice], ', "ask":', $y[askPrice], '},';

	$x = file_get_contents('https://www.bitstamp.net/api/v2/ticker/btcusd', false, $context); 
	$y = json_decode($x,true); 
	echo '{"exchange":"bitstamp", "bid":', $y[bid], ', "ask":', $y[ask], '},';

	$x = file_get_contents('https://cex.io/api/ticker/BTC/USD', false, $context); 
	$y = json_decode($x,true); 
	echo '{"exchange":"cex", "bid":', $y[bid], ', "ask":', $y[ask], '},';

	$x = file_get_contents('https://api.gdax.com/products/BTC-USD/ticker', false, $context); 
	$y = json_decode($x,true); 
	echo '{"exchange":"gdax", "bid":', $y[bid], ', "ask":', $y[ask], '},';

/*
	$x = file_get_contents('https://api.hitbtc.com/api/2/public/ticker/BTCUSD', false, $context); 
	$y = json_decode($x,true); 
	echo '{"exchange":"hitbtc", "bid":', $y[bid], ', "ask":', $y[ask], '},';
*/

	$x = file_get_contents('https://api.kucoin.com/v1/open/tick?symbol=BTC-USDT', false, $context); 
	$y = json_decode($x,true); 
	echo '{"exchange":"kucoin", "bid":', $y[data][buy], ', "ask":', $y[data][sell], '},';

	$x = file_get_contents('https://api.exmo.com/v1/ticker', false, $context); 
	$y = json_decode($x,true); 
	echo '{"exchange":"exmo", "bid":', $y[BTC_USDT][buy_price], ', "ask":', $y[BTC_USDT][sell_price], '}';
	echo ']}';
?>
