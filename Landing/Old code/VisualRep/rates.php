<?php
	error_reporting(0);
	// JSON array of (bourse, bid, ask)
	$options  = array('http' => array('user_agent' => 'curl/7.29.0'));
	$context  = stream_context_create($options);
	echo '{ "list": [';
	ini_set('default_socket_timeout', 1);


	try {
		$x = file_get_contents('https://api.binance.com/api/v3/ticker/bookTicker?symbol=BTCUSDT', false, $context);
		$y = json_decode($x,true);
		if (isset($y['bidPrice']) && isset($y['askPrice'])) {
			echo '{"exchange":"binance (USDT)", "bid":', $y['bidPrice'], ', "ask":', $y['askPrice'], '},';
		}
		else {
			echo '{"exchange":"binance (USDT)", "bid":0, "ask":0},';
		}
	}
	catch(Exception $e) {
		echo '{"exchange":"binance (USDT)", "bid":0, "ask":0},';
	}


	try {
		$x = file_get_contents('https://www.bitstamp.net/api/v2/ticker/btcusd', false, $context); 
		$y = json_decode($x,true);
		if (isset($y['bid']) && isset($y['ask'])) {
			echo '{"exchange":"bitstamp (USD)", "bid":', $y['bid'], ', "ask":', $y['ask'], '},';
		}
		else {
			echo '{"exchange":"bitstamp (USD)", "bid":0, "ask":0},';
		}
	}
	catch(Exception $e) {
		echo '{"exchange":"bitstamp (USD)", "bid":0, "ask":0},';
	}


	try {
		$x = file_get_contents('https://cex.io/api/ticker/BTC/USD', false, $context); 
		$y = json_decode($x,true); 
		if (isset($y['bid']) && isset($y['ask'])) {
			echo '{"exchange":"cex (USD)", "bid":', $y['bid'], ', "ask":', $y['ask'], '},';
		}
		else {
			echo '{"exchange":"cex (USD)", "bid":0, "ask":0},';
		}
	}
	catch(Exception $e) {
		echo '{"exchange":"cex (USD), "bid":0, "ask":0},';
	}


	try {
		$x = file_get_contents('https://api.gdax.com/products/BTC-USD/ticker', false, $context); 
		$y = json_decode($x,true); 
		if (isset($y['bid']) && isset($y['ask'])) {
			echo '{"exchange":"gdax (USD)", "bid":', $y['bid'], ', "ask":', $y['ask'], '},';
		}
		else {
			echo '{"exchange":"gdax (USD)", "bid":0, "ask":0},';
		}
	}
	catch(Exception $e) {
		echo '{"exchange":"gdax (USD)", "bid":0, "ask":0},';
	}

/*
	$x = file_get_contents('https://api.hitbtc.com/api/2/public/ticker/BTCUSD', false, $context); 
	$y = json_decode($x,true); 
	echo '{"exchange":"hitbtc", "bid":', $y['bid'], ', "ask":', $y['ask'], '},';
*/

	try {
		$x = file_get_contents('https://api.kucoin.com/v1/open/tick?symbol=BTC-USDT', false, $context); 
		$y = json_decode($x,true); 
		if (isset($y['data'])) {
			if (isset($y['data']['buy']) && isset($y['data']['sell'])) {
				echo '{"exchange":"kucoin (USDT)", "bid":', $y['data']['buy'], ', "ask":', $y['data']['sell'], '},';
			}
			else {
				echo '{"exchange":"kucoin (USDT)", "bid":0, "ask":0},';
			}
		}
		else {
			echo '{"exchange":"kucoin (USDT)", "bid":0, "ask":0},';
		}
	}
	catch(Exception $e) {
		echo '{"exchange":"kucoin (USDT)", "bid":0, "ask":0},';
	}


	try {
		$x = file_get_contents('https://api.exmo.com/v1/ticker', false, $context); 
		$y = json_decode($x,true); 
		if (isset($y['BTC_USDT'])) {
			if (isset($y['BTC_USDT']['buy_price']) && isset($y['BTC_USDT']['sell_price'])) {
				echo '{"exchange":"exmo (USDT)", "bid":', $y['BTC_USDT']['buy_price'], ', "ask":', $y['BTC_USDT']['sell_price'], '},';
			}
			else {
				echo '{"exchange":"exmo (USDT)", "bid":0, "ask":0},';
			}
		}
		else {
			echo '{"exchange":"exmo (USDT)", "bid":0, "ask":0},';
		}
	}
	catch(Exception $e) {
		echo '{"exchange":"exmo (USDT)", "bid":0, "ask":0},';
	}


	try {
		$x = file_get_contents('https://api.exmo.com/v1/ticker', false, $context); 
		$y = json_decode($x,true); 
		if (isset($y['BTC_USD'])) {
			if (isset($y['BTC_USD']['buy_price']) && isset($y['BTC_USD']['sell_price'])) {
				echo '{"exchange":"exmo (USD)", "bid":', $y['BTC_USD']['buy_price'], ', "ask":', $y['BTC_USD']['sell_price'], '}';
			}
			else {
				echo '{"exchange":"exmo (USD)", "bid":0, "ask":0}';
			}
		}
		else {
			echo '{"exchange":"exmo (USD)", "bid":0, "ask":0}';
		}
	}
	catch(Exception $e) {
		echo '{"exchange":"exmo (USD)", "bid":0, "ask":0}';
	}


	echo ']}';
?>
