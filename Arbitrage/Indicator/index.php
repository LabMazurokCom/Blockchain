<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>Rate comparator</title>
		<script>
			function get_rates() {
				var xhr = new XMLHttpRequest();
				xhr.open('GET', 'rates.php', true);
				xhr.onload = function() {
	                var response = JSON.parse(this.responseText).list;
//	                console.log("response.list");
//	                console.log(response);
	                a = [];
	                for (var ix in response) {
						a.push({
						"exchange" : response[ix].exchange,
						"bid": 0,
						"ask": response[ix].ask
						});
						a.push({
						"exchange" : response[ix].exchange,
						"bid": response[ix].bid,
						"ask": 0
						});
	                }
//	                console.log("Array a");
//	                console.log(a);
	                a.sort(function(x,y){
						return x.bid + x.ask - y.bid - y.ask;
	                });
//	                console.log("After sorting");
//	                console.log(a);
	                var first_ask = 0;
	                var last_bid = 0;
	                for (var ix in a) {
	                	if (a[ix].bid == 0) {
	                		document.getElementById("ask" + ix.toString()).innerHTML = a[ix].ask;
	                		document.getElementById("right" + ix.toString()).innerHTML = a[ix].exchange;
	                		if (first_ask == 0)
	                			first_ask = a[ix].ask;
	                	}
	                	else {
	                 		document.getElementById("bid" + ix.toString()).innerHTML = a[ix].bid;
	                		document.getElementById("left" + ix.toString()).innerHTML = a[ix].exchange;  
	                		last_bid = a[ix].bid;           
	                	}
	                }
	                console.log("First Ask", first_ask);
	                console.log("Last Bid", last_bid);
	                if (first_ask < last_bid) {
	                	var val = 100 * (last_bid - first_ask) / first_ask;
		                document.getElementById("percent_change").innerHTML = val.toString() + "%";  
	                }
		            else
		            	document.getElementById("percent_change").innerHTML = "No Arbitrage"; 
				}
				xhr.onerror = function() {
				  alert('Error ' + this.status);
				}
				xhr.send();
			}
		</script>
</head>
	<body onload="get_rates()">
		<h1 id="percent_change"> </h1>
		<table border = 1>
		<tr>
			<th width="20%"> Exchange From </th>
			<th width="20%" style = "color:blue"> Bid </th>
			<th width="20%" style = "color:red"> Ask </th>
			<th width="20%"> Exchange To </th>
		</tr>
		<tr>
			<td id="left0"> </td>
			<td id="bid0"> </td>
			<td id="ask0"> </td>
			<td id="right0"> </td>
		</tr>
		<tr>
			<td id="left1"> </td>
			<td id="bid1"> </td>
			<td id="ask1"> </td>
			<td id="right1"> </td>
		</tr>
		<tr>
			<td id="left2"> </td>
			<td id="bid2"> </td>
			<td id="ask2"> </td>
			<td id="right2"> </td>
		</tr>
		<tr>
			<td id="left3"> </td>
			<td id="bid3"> </td>
			<td id="ask3"> </td>
			<td id="right3"> </td>
		</tr>
		<tr>
			<td id="left4"> </td>
			<td id="bid4"> </td>
			<td id="ask4"> </td>
			<td id="right4"> </td>
		</tr>
		<tr>
			<td id="left5"> </td>
			<td id="bid5"> </td>
			<td id="ask5"> </td>
			<td id="right5"> </td>
        </tr>
		<tr>
			<td id="left6"> </td>
			<td id="bid6"> </td>
			<td id="ask6"> </td>
			<td id="right6"> </td>
		</tr>
		<tr>
			<td id="left7"> </td>
			<td id="bid7"> </td>
			<td id="ask7"> </td>
			<td id="right7"> </td>
		</tr>
		<tr>
			<td id="left8"> </td>
			<td id="bid8"> </td>
			<td id="ask8"> </td>
			<td id="right8"> </td>
		</tr>
		<tr>
			<td id="left9"> </td>
			<td id="bid9"> </td>
			<td id="ask9"> </td>
			<td id="right9"> </td>
		</tr>
		<tr>
			<td id="left10"> </td>
			<td id="bid10"> </td>
			<td id="ask10"> </td>
			<td id="right10"> </td>
		</tr>
		<tr>
			<td id="left11"> </td>
			<td id="bid11"> </td>
			<td id="ask11"> </td>
			<td id="right11"> </td>
		</tr>
		</table>
	</body>
</html>