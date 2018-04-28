<?php
	$options  = array('http' => array('user_agent' => 'curl/7.29.0'));
	$context  = stream_context_create($options);
	error_reporting(0);

	try {
		$x = file_get_contents('https://arbitrage-logger.firebaseio.com/log_btc_usd.json?orderBy=%22$key%22&limitToLast=1', false, $context);
		echo $x, '<br/><br/>';
		// $y = json_decode($x, true);
		// print_r($y);
	}
	catch(Exception $e) {
		echo '{"exchange":"binance (USDT)", "bid":0, "ask":0},';
	}
?>
