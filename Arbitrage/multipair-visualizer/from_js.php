<html>
<head>
	<title>
		Hello, Firebase!
	</title>
	<script>
		function reqListener () {
			console.log(this.responseText);
			console.log("\n\n")
			console.log(this.headers);
		}
		var xhr = new XMLHttpRequest();
		xhr.addEventListener('load', reqListener);
		xhr.open('GET', 'https://arbitrage-logger.firebaseio.com/log_btc_usd.json?orderBy=%22$key%22&limitToLast=1&print=pretty');
		xhr.send();
		//xhr.setRequestHeader('foo','bar');
	</script>	
</head>
<body>
</body>
</html>