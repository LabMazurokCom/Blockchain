<?php
	// echoes {"ticker":[{exchange name, bid, ask}, {}, ..., {}], "profit": float, "volume": volume}
	$options  = array('http' => array('user_agent' => 'curl/7.29.0'));
	$context  = stream_context_create($options);
	echo '{ "ticker": [';
	error_reporting(0);
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
			/*
			for($i = 0; $i < min($Limit, count($y['bids'])); $i++) {
				array_push($bids, [$y['bids'][$i][0], $y['bids'][$i][1]]);				
			}
			for($i = 0; $i < min($Limit, count($y['asks'])); $i++) {
				array_push($asks, [$y['asks'][$i][0], $y['asks'][$i][1]]);				
			}
			*/		
			foreach($y['bids'] as $cur_bid) {
				array_push($bids, [$cur_bid[0], $cur_bid[1]]);
			}
			foreach($y['asks'] as $cur_ask) {
				array_push($asks, [$cur_ask[0], $cur_ask[1]]);		
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
		$x = file_get_contents('https://www.bitstamp.net/api/v2/order_book/btcusd/', false, $context); 
		$y = json_decode($x,true);
		if (isset($y['bids']) && isset($y['asks'])) {	
			for($i = 0; $i < min($Limit, count($y['bids'])); $i++) {
				array_push($bids, [$y['bids'][$i][0], $y['bids'][$i][1]]);
			}
			for($i = 0; $i < min($Limit, count($y['asks'])); $i++) {
				array_push($asks, [$y['asks'][$i][0], $y['asks'][$i][1]]);			
			}
			/*
			foreach($y['bids'] as $cur_bid) {
				array_push($bids, [$cur_bid[0], $cur_bid[1]]);
			}
			foreach($y['asks'] as $cur_ask) {
				array_push($asks, [$cur_ask[0], $cur_ask[1]]);				
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
			/*
			for($i = 0; $i < min($Limit, count($y['bids'])); $i++) {
				array_push($bids, $y['bids'][$i]);				
			}
			for($i = 0; $i < min($Limit, count($y['asks'])); $i++) {
				array_push($asks, $y['asks'][$i]);	
			}
			*/
			foreach($y['bids'] as $cur_bid) {
				array_push($bids, [$cur_bid[0], $cur_bid[1]]);
			}
			foreach($y['asks'] as $cur_ask) {
				array_push($asks, [$cur_ask[0], $cur_ask[1]]);				
			}
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
			/*
			for($i = 0; $i < min($Limit, count($y['bids'])); $i++) {
				array_push($bids, $y['bids'][$i]);				
			}
			for($i = 0; $i < min($Limit, count($y['asks'])); $i++) {
				array_push($asks, $y['asks'][$i]);	
			}
			*/
			foreach($y['bids'] as $cur_bid) {
				array_push($bids, [$cur_bid[0], $cur_bid[1]]);
			}
			foreach($y['asks'] as $cur_ask) {
				array_push($asks, [$cur_ask[0], $cur_ask[1]]);				
			}
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
				foreach($y['BUY'] as $cur_bid) {
					array_push($bids, [$cur_bid[0], $cur_bid[1]]);
				}
				foreach($y['SELL'] as $cur_ask) {
					array_push($asks, [$cur_ask[0], $cur_ask[1]]);		
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
				foreach($y['bid'] as $cur_bid) {
					array_push($bids, [$cur_bid[0], $cur_bid[1]]);
				}
				foreach($y['ask'] as $cur_ask) {
					array_push($asks, [$cur_ask[0], $cur_ask[1]]);
				}
				echo '{"exchange":"exmo (USD)", "bid":', $y['bid'][0][0], ', "ask":', $y['ask'][0][0], '},';
			}
			else {
				echo '{"exchange":"exmo (USD)", "bid":0, "ask":0},';
			}
		}
		else {
			echo '{"exchange":"exmo (USD)", "bid":0, "ask":0},';
		}
	}
	catch(Exception $e) {
		echo '{"exchange":"exmo (USD)", "bid":0, "ask":0},';
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
				foreach($y['bid'] as $cur_bid) {
					array_push($bids, [$cur_bid[0], $cur_bid[1]]);
				}
				foreach($y['ask'] as $cur_ask) {
					array_push($asks, [$cur_ask[0], $cur_ask[1]]);
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


	rsort($bids);
	sort($asks);


	$bx = 0;
	$ax = 0;
	$bid_count = count($bids);
	$ask_count = count($asks);
	$profit = 0;
	$usd_amount = 0;
	$trade_cnt = 0;
	$profit_points = array();
	$amount_points = array();

	$alpha = 0.1;
	$prev_diff = 1e-6;
	$optimal_amount = 0;
	$optimal_profit = 0;

	$num = 0;


	while ($bx < $bid_count  &&  $ax < $ask_count  &&  $bids[$bx][0] > $asks[$ax][0]) {
		$bid_vol = $bids[$bx][1];
		$ask_vol = $asks[$ax][1];
		if ($bid_vol == 0) {
			$bx++;
			continue;
		}
		if ($ask_vol == 0) {
			$ax++;
			continue;
		}


		$m = min($bid_vol, $ask_vol);
		$current_profit = ($bids[$bx][0] - $asks[$ax][0]) * $m;
		$profit += $current_profit;
		$usd_amount += $asks[$ax][0] * $m;
		array_push($profit_points, $profit);
		array_push($amount_points, $usd_amount);
//		echo 'trade: ', $bids[$bx][0] - $asks[$ax][0], ' ', $m, ', profit = ', $current_profit, '    <br/>';
		$bids[$bx][1] -= $m;
		$asks[$ax][1] -= $m;
		$trade_cnt += 1;


		$num++;
		if ($num == 1) {
			$prev_amount = $usd_amount;
			$prev_profit = $profit;
		}
		elseif ($num == 2) {
			$first_k = ($profit - $prev_profit) / ($usd_amount - $prev_amount);
			$prev_amount = $usd_amount;
			$prev_profit = $profit;
		}
		else {
			$k = ($profit - $prev_profit) / ($usd_amount - $prev_amount);
			if ($k / $first_k >= $alpha) {
				$optimal_amount = $usd_amount;
				$optimal_profit = $profit;	
			}
			$prev_amount = $usd_amount;
			$prev_profit = $profit;
		}
/*
		$num++;
		if ($num > 2) {
			$k = ($profit - $prev_profit) / ($usd_amount - $prev_amount);
			echo $prev_k, ',  ', $k, ',  ', ($prev_k - $k) / $prev_k, '<br/>';	/// $prev_k, '<br/>';
			if (($prev_k - $k) / $prev_k >= $alpha) {
				$optimal_amount = $usd_amount;
				$optimal_profit = $profit;				
			}
			$prev_k = $k;
			$prev_amount = $usd_amount;
			$prev_profit = $profit;		
		}
		elseif ($num == 2) {
			$prev_k = ($profit - $prev_profit) / ($usd_amount - $prev_amount);
			$prev_amount = $usd_amount;
			$prev_profit = $profit;			
		}
		else {
			$prev_amount = $usd_amount;
			$prev_profit = $profit;
		}
*/
/*
		$current_diff = abs($bids[$bx][0] - $asks[$ax][0]) / $asks[$ax][0];
		if (abs($current_diff - $prev_diff) / $prev_diff >= $alpha) {
			$optimal_amount = $usd_amount;
			$optimal_profit = $profit;
		}
		echo '<br/>', $bids[$bx][0], ',  ', $asks[$ax][0], '  --  ';	//, $current_diff, '<br/>';
		echo $prev_diff, ',  ', $current_diff, ',  ', abs($current_diff - $prev_diff) / $prev_diff, '<br/>';
		$prev_diff = $current_diff;
*/
	}


	echo '], ';
	echo '"profit":', $profit, ', ';
	echo '"trade_cnt":', $trade_cnt, ', ';
	echo '"usd_amount":', $usd_amount, ', ';
	echo '"optimal_point":{"amount":', $optimal_amount, ', "profit":', $optimal_profit, '}, ';

	echo '"amount_points": [';
	for ($i = 0; $i < $trade_cnt; $i++) {
		echo $amount_points[$i];
		if ($i < $trade_cnt - 1)
			echo ', ';
		else
			echo '], ';
	}
	echo '"profit_points": [';
	$n_prof = count($profit_points);
	for ($i = 0; $i < $trade_cnt; $i++) {
		echo $profit_points[$i];
		if ($i < $trade_cnt - 1)
			echo ', ';
		else
			echo ']';
	}
	echo '}';
/*
	echo '<br/><br/>';
	for($i = 0; $i < min(count($bids), count($asks)); $i++) {
		echo $i, '  ';
		if ($bids[$i][0] > $asks[$i][0])
			echo '<span style="color: green;">';
		else
			echo '<span style="color: red;">';
		echo $bids[$i][0], ' ', $bids[$i][1], ' ........ ', $asks[$i][0], ' ', $asks[$i][1], '</span><br/>';
	}
*/
?>