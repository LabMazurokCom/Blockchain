<?php
//	Binance

  $options  = array(‘http’ => array(‘user_agent’ => ‘curl/7.29.0’));

  $context  = stream_context_create($options);
  // error_reporting(0);
	try {
		// Valid limits:[5, 10, 20, 50, 100, 500, 1000], limit = 0  -->  all orders
		$x = file_get_contents('https://arbitrage-logger.firebaseio.com/log_btc_usd.json?orderBy=%22$key%22&limitToLast=1', false, $context);
//		$x = file_get_contents('https://api.binance.com/api/v1/depth?symbol=BTCUSDT&limit=0', false, $context);		// all orders
		$y = json_decode($x,true);

    echo $x;
    echo '<br></br>';
    echo $y;


	}
	catch(Exception $e) {
		echo $e;
	}


?>
