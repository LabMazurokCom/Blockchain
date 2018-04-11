<?php
	// echoes {"ticker":[{exchange name, bid, ask}, {}, ..., {}], "profit": float, "volume": volume}
	$options  = array('http' => array('user_agent' => 'curl/7.29.0'));
	$context  = stream_context_create($options);
//	echo '{ "ticker": [';
//	ini_set('default_socket_timeout', 10);

	$bids = array();
	$asks = array();
	$Limit = 50;


//	Binance
	try {
		// Valid limits:[5, 10, 20, 50, 100, 500, 1000], limit = 0  -->  all orders
		$x = file_get_contents('https://api.binance.com/api/v1/depth?symbol=BTCUSDT&limit=50', false, $context);		
//		$x = file_get_contents('https://api.binance.com/api/v1/depth?symbol=BTCUSDT&limit=0', false, $context);		// all orders
		$y = json_decode($x,true);

		if (isset($y['bids']) && isset($y['asks'])) {
			echo '<br/><br/>Binance<br/>';
			/*
			for($i = 0; $i < min($Limit, count($y['bids'])); $i++) {
				array_push($bids, [$y['bids'][$i][0], $y['bids'][$i][1]]);				
			}
			for($i = 0; $i < min($Limit, count($y['asks'])); $i++) {
				array_push($asks, [$y['asks'][$i][0], $y['asks'][$i][1]]);				
			}
			*/		
			$i = 0;
			foreach($y['bids'] as $cur_bid) {
				array_push($bids, [$i, 'Binance', $cur_bid[0], $cur_bid[1]]);
				$i++;
			}
			$i = 0;
			foreach($y['asks'] as $cur_ask) {
				array_push($asks, [$i, 'Binance', $cur_ask[0], $cur_ask[1]]);		
				$i++;		
			}
			echo '{"exchange":"binance (USDT)", "bid":', $y['bids'][0][0], ', "ask":', $y['asks'][0][0], '},';
		}
		else {
			echo '{"exchange":"binance (USDT)", "bid":0, "ask":0},';
		}
	}
	catch(Exception $e) {
		echo '{"exchange":"binance (USDT)", "bid":0, "ask":0},';
	}


//	Bitstamp
	try {
		$x = file_get_contents('https://www.bitstamp.net/api/v2/order_book/btcusd/?limit=50', false, $context); 
		$y = json_decode($x,true);
		if (isset($y['bids']) && isset($y['asks'])) {		
			for($i = 0; $i < min($Limit, count($y['bids'])); $i++) {
				array_push($bids, [$i, 'Bitstamp', $y['bids'][$i][0], $y['bids'][$i][1]]);
			//	array_push($bids, $y['bids'][$i]);				
			}
			for($i = 0; $i < min($Limit, count($y['asks'])); $i++) {
				array_push($asks, [$i, 'Bitstamp', $y['asks'][$i][0], $y['asks'][$i][1]]);			
			//	array_push($asks, $y['asks'][$i]);	
			}
			/*
			foreach($y['bids'] as $cur_bid) {
				array_push($bids, $cur_bid);
			}
			echo 'Asks', count($y['asks']), '<br/>';
			foreach($y['asks'] as $cur_ask) {
				array_push($asks, $cur_ask);				
			}
			*/
			echo '{"exchange":"bitstamp (USD)", "bid":', $y['bids'][0][0], ', "ask":', $y['asks'][0][0], '},';
		}
		else {
			echo '{"exchange":"bitstamp (USD)", "bid":0, "ask":0},';
		}
	}
	catch(Exception $e) {
		echo '{"exchange":"bitstamp (USD)", "bid":0, "ask":0},';
	}


//	CEX
	try {
		$x = file_get_contents('https://cex.io/api/order_book/BTC/USD/?depth=50', false, $context); 
//		$x = file_get_contents('https://cex.io/api/order_book/BTC/USD', false, $context); 	// all orders
		$y = json_decode($x,true); 
		if (isset($y['bids']) && isset($y['asks'])) {
			for($i = 0; $i < min($Limit, count($y['bids'])); $i++) {
				array_push($bids, [$i, 'CEX', $y['bids'][$i][0], $y['bids'][$i][1]]);
			//	array_push($bids, $y['bids'][$i]);				
			}
			for($i = 0; $i < min($Limit, count($y['asks'])); $i++) {
				array_push($asks, [$i, 'CEX', $y['asks'][$i][0], $y['asks'][$i][1]]);			
			//	array_push($asks, $y['asks'][$i]);	
			}
			/*
			foreach($y['bids'] as $cur_bid) {
				array_push($bids, $cur_bid);
			}
			echo 'Asks', count($y['asks']), '<br/>';
			foreach($y['asks'] as $cur_ask) {
				array_push($asks, $cur_ask);				
			}
			*/
			echo '{"exchange":"cex (USD)", "bid":', $y['bids'][0][0], ', "ask":', $y['asks'][0][0], '},';
		}
		else {
			echo '{"exchange":"cex (USD)", "bid":0, "ask":0},';
		}
	}
	catch(Exception $e) {
		echo '{"exchange":"cex (USD)", "bid":0, "ask":0},';
	}


//	GDAX
	try {
		$x = file_get_contents('https://api.gdax.com/products/BTC-USD/book?level=2', false, $context); 		// top 50 prices with aggregated volumes
//		$x = file_get_contents('https://api.gdax.com/products/BTC-USD/book?level=3', false, $context); 		// all orders

		$y = json_decode($x,true); 
		if (isset($y['bids']) && isset($y['asks'])) {
			for($i = 0; $i < min($Limit, count($y['bids'])); $i++) {
				array_push($bids, [$i, 'GDAX', $y['bids'][$i][0], $y['bids'][$i][1]]);
			//	array_push($bids, $y['bids'][$i]);				
			}
			for($i = 0; $i < min($Limit, count($y['asks'])); $i++) {
				array_push($asks, [$i, 'GDAX', $y['asks'][$i][0], $y['asks'][$i][1]]);			
			//	array_push($asks, $y['asks'][$i]);	
			}
			/*
			foreach($y['bids'] as $cur_bid) {
				array_push($bids, [$cur_bid[0], $cur_bid[1]]);
			}
			echo 'Asks', count($y['asks']), '<br/>';
			foreach($y['asks'] as $cur_ask) {
				array_push($asks, [$cur_ask[0], $cur_ask[1]]);				
			}
			*/
			echo '{"exchange":"gdax (USD)", "bid":', $y['bids'][0][0], ', "ask":', $y['asks'][0][0], '},';
		}
		else {
			echo '{"exchange":"gdax (USD)", "bid":0, "ask":0},';
		}
	}
	catch(Exception $e) {
		echo '{"exchange":"gdax (USD)", "bid":0, "ask":0},';
	}


//	KuCoin
	try {
		$x = file_get_contents('https://api.kucoin.com/v1/open/orders?symbol=BTC-USDT&limit=50', false, $context); 			// can't get more than 100 orders
//		$x = file_get_contents('https://api.kucoin.com/v1/open/orders-buy?symbol=BTC-USDT&limit=200', false, $context); 	// can't get more than 200 orders
//		$x = file_get_contents('https://api.kucoin.com/v1/open/orders-sell?symbol=BTC-USDT&limit=200', false, $context); 	// can't get more than 200 orders
		$y = json_decode($x,true);
		if (isset($y['data'])) {
			$y = $y['data'];
			if (isset($y['BUY']) && isset($y['BUY'])) {
				/*
				for($i = 0; $i < min($Limit, count($y['BUY'])); $i++) {
					array_push($bids, [$y['BUY'][$i][0], $y['BUY'][$i][1]]);				
				}
				for($i = 0; $i < min($Limit, count($y['SELL'])); $i++) {
					array_push($asks, [$y['SELL'][$i][0], $y['SELL'][$i][1]]);				
				}
				*/
				$i = 0;
				foreach($y['BUY'] as $cur_bid) {
					array_push($bids, [$i, 'KuCoin', $cur_bid[0], $cur_bid[1]]);
					$i++;
				}
				$i = 0;
				foreach($y['SELL'] as $cur_ask) {
					array_push($asks, [$i, 'KuCoin', $cur_ask[0], $cur_ask[1]]);		
					$i++;		
				}
				echo '{"exchange":"kucoin (USDT)", "bid":', $y['BUY'][0][0], ', "ask":', $y['SELL'][0][0], '},';
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


//	EXMO (USD)
	try {
		$x = file_get_contents('https://api.exmo.com/v1/order_book/?pair=BTC_USD&limit=50', false, $context); 		// no more than 1000 orders
		$y = json_decode($x,true); 
		if (isset($y['BTC_USD'])) {
			$y = $y['BTC_USD'];
			if (isset($y['bid']) && isset($y['ask'])) {
				/*
				for($i = 0; $i < min($Limit, count($y['bid'])); $i++) {
					array_push($bids, [$y['bid'][$i][0], $y['bid'][$i][1]]);				
				}
				for($i = 0; $i < min($Limit, count($y['ask'])); $i++) {
					array_push($asks, [$y['ask'][$i][0], $y['ask'][$i][1]]);				
				}
				*/
				$i = 0;
				foreach($y['bid'] as $cur_bid) {
					array_push($bids, [$i, 'EXMO (USD)', $cur_bid[0], $cur_bid[1]]);
					$i++;
				}
				$i = 0;
				foreach($y['ask'] as $cur_ask) {
					array_push($asks, [$i, 'EXMO (USD)', $cur_ask[0], $cur_ask[1]]);
					$i++;
				}
				echo '{"exchange":"exmo (USD)", "bid":', $y['bid'][0][0], ', "ask":', $y['ask'][0][0], '}';
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


//	EXMO (USDT)
	try {
		$x = file_get_contents('https://api.exmo.com/v1/order_book/?pair=BTC_USDT&limit=50', false, $context); 		// no more than 1000 orders
		$y = json_decode($x,true); 
		if (isset($y['BTC_USDT'])) {
			$y = $y['BTC_USDT'];
			if (isset($y['bid']) && isset($y['ask'])) {
				/*
				for($i = 0; $i < min($Limit, count($y['bid'])); $i++) {
					array_push($bids, [$y['bid'][$i][0], $y['bid'][$i][1]]);				
				}
				for($i = 0; $i < min($Limit, count($y['ask'])); $i++) {
					array_push($asks, [$y['ask'][$i][0], $y['ask'][$i][1]]);				
				}
				*/
				$i = 0;
				foreach($y['bid'] as $cur_bid) {
					array_push($bids, [$i, 'EXMO (USDT)', $cur_bid[0], $cur_bid[1]]);
					$i++;
				}
				$i = 0;
				foreach($y['ask'] as $cur_ask) {
					array_push($asks, [$i, 'EXMO (USDT)', $cur_ask[0], $cur_ask[1]]);
					$i++;	
				}
				echo '{"exchange":"exmo (USDT)", "bid":', $y['bid'][0][0], ', "ask":', $y['ask'][0][0], '}';
			}
			else {
				echo '{"exchange":"exmo (USDT)", "bid":0, "ask":0}';
			}
		}
		else {
			echo '{"exchange":"exmo (USDT)", "bid":0, "ask":0}';
		}
	}
	catch(Exception $e) {
		echo '{"exchange":"exmo (USDT)", "bid":0, "ask":0}';
	}

	echo '], ';
	$profit = 1000000;
	echo '"profit":', $profit, ', ';
	$volume = 1;
	echo '"volume":', $volume, '}';


	echo('<br/><br/>');
	echo('BIDS<br/>');
	foreach($bids as $cur_bid)
		echo $cur_bid[0], ' ', $cur_bid[1], ' ', $cur_bid[2], ' ', $cur_bid[3], '<br/>';
	echo('<br/><br/>');
	echo('ASKS<br/>');
	foreach($asks as $cur_ask)
		echo $cur_ask[0], ' ', $cur_ask[1], ' ', $cur_ask[2], ' ', $cur_ask[3], '<br/>';
?>
