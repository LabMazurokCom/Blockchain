<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <link rel="stylesheet" type="text/css" href="mystyle.css">
    <title>Rate comparator</title>
		<script>
			function get_rates() {
				var xhr = new XMLHttpRequest();
				xhr.open('GET', 'rates.php', true);
				xhr.onload = function() {
	                var response = JSON.parse(this.responseText).list;
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
	                a.sort(function(x,y){
						return -(x.bid + x.ask - y.bid - y.ask);
	                });
	                var first_ask = 0;
	                var last_ask = 0;
	                var first_ask_ix = -1;
	                var last_ask_ix = 0;
	                var first_bid = 0;
	                var last_bid = 0;
	                var first_bid_ix = -1;
	                var last_bid_ix = 0;
	                var tmp;
	                for (var ix in a) {
	                	if (a[ix].bid == 0) {
	                		tmp = parseFloat(a[ix].ask);
	                		document.getElementById("ask" + ix.toString()).innerHTML = tmp.toFixed(2);
	                		document.getElementById("right" + ix.toString()).innerHTML = a[ix].exchange;
	                		if (first_ask == 0) {
	                			first_ask = a[ix].ask;
	                			first_ask_ix = ix;
	                		}
	                		last_ask_ix = ix;
	                		last_ask = a[ix].ask;
	                	}
	                	else {
	                		tmp = parseFloat(a[ix].bid);
	                 		document.getElementById("bid" + ix.toString()).innerHTML = tmp.toFixed(2);
	                		document.getElementById("left" + ix.toString()).innerHTML = a[ix].exchange;  
	                		if (first_bid_ix == -1) {
	                			first_bid_ix = ix;
	                			first_bid = a[ix].bid;
	                		}
	                		last_bid = a[ix].bid;
	                		last_bid_ix = ix;           
	                	}
	                }

	                if (last_ask < first_bid) {
	                	var val = 100 * (first_bid - last_ask) / last_ask;
	                	val = val.toFixed(2);
		                document.getElementById("percent_change").innerHTML = val.toString() + "%";

						var bx = parseInt(first_bid_ix);
						var ax = parseInt(last_ask_ix);
						while (a[bx].bid >= a[ax].ask) {
		                	document.getElementById("ask" + ax.toString()).style.backgroundColor = "rgb(255,195,225)";
		                	document.getElementById("right" + ax.toString()).style.backgroundColor = "rgb(255,195,225)";
		                	document.getElementById("bid" + bx.toString()).style.backgroundColor = "rgb(177,252,177)";
		                	document.getElementById("left" + bx.toString()).style.backgroundColor = "rgb(177,252,177)";	
		                	bx++;
		                	while (a[bx].bid == 0)
		                		bx++;
		                	ax--;
		                	while (a[ax].ask == 0)
			                	ax--;						
						}
		                
		                document.getElementById("leftmid" + first_bid_ix).style.borderTopStyle = "solid";
		               	document.getElementById("leftmid" + first_bid_ix).style.borderTopWidth = "3px";
		               	document.getElementById("leftmid" + first_bid_ix).style.borderTopColor = "green"; 
		                document.getElementById("rightmid" + first_bid_ix).style.borderTopStyle = "solid";
		               	document.getElementById("rightmid" + first_bid_ix).style.borderTopWidth = "3px";
		               	document.getElementById("rightmid" + first_bid_ix).style.borderTopColor = "green";		               			               	
		                for (var kx = parseInt(first_bid_ix); kx <= parseInt(last_ask_ix); kx++) {
		                	document.getElementById("leftmid" + kx.toString()).style.backgroundColor = "green";
		                	document.getElementById("rightmid" + kx.toString()).style.backgroundColor = "green";
		            	}
		                document.getElementById("leftmid" + last_ask_ix).style.borderBottomStyle = "solid";
		               	document.getElementById("leftmid" + last_ask_ix).style.borderBottomWidth = "3px";
		               	document.getElementById("leftmid" + last_ask_ix).style.borderBottomColor = "green";	 
		                document.getElementById("rightmid" + last_ask_ix).style.borderBottomStyle = "solid";
		               	document.getElementById("rightmid" + last_ask_ix).style.borderBottomWidth = "3px";
		               	document.getElementById("rightmid" + last_ask_ix).style.borderBottomColor = "green";			         
						


		                document.getElementById("left" + first_bid_ix).style.borderTopStyle = "solid";
		               	document.getElementById("left" + first_bid_ix).style.borderTopWidth = "3px";
		               	document.getElementById("left" + first_bid_ix).style.borderTopColor = "green"; 
		                document.getElementById("bid" + first_bid_ix).style.borderTopStyle = "solid";
		               	document.getElementById("bid" + first_bid_ix).style.borderTopWidth = "3px";
		               	document.getElementById("bid" + first_bid_ix).style.borderTopColor = "green";

		                for (var kx = parseInt(first_bid_ix); kx <= parseInt(last_bid_ix); kx++) {
		                	document.getElementById("left" + kx.toString()).style.borderLeftStyle = "solid";
		                	document.getElementById("left" + kx.toString()).style.borderLeftWidth = "3px";
		                	document.getElementById("left" + kx.toString()).style.borderLeftColor = "green"; 

		                	document.getElementById("bid" + kx.toString()).style.borderRightStyle = "solid";
		                	document.getElementById("bid" + kx.toString()).style.borderRightWidth = "3px";
		                	document.getElementById("bid" + kx.toString()).style.borderRightColor = "green";
		                }

		                document.getElementById("left" + last_bid_ix).style.borderBottomStyle = "solid";
		               	document.getElementById("left" + last_bid_ix).style.borderBottomWidth = "3px";
		               	document.getElementById("left" + last_bid_ix).style.borderBottomColor = "green"; 
		                document.getElementById("bid" + last_bid_ix).style.borderBottomStyle = "solid";
		               	document.getElementById("bid" + last_bid_ix).style.borderBottomWidth = "3px";
		               	document.getElementById("bid" + last_bid_ix).style.borderBottomColor = "green"; 



		                document.getElementById("ask" + first_ask_ix).style.borderTopStyle = "solid";
		               	document.getElementById("ask" + first_ask_ix).style.borderTopWidth = "3px";
		               	document.getElementById("ask" + first_ask_ix).style.borderTopColor = "red"; 
		                document.getElementById("right" + first_ask_ix).style.borderTopStyle = "solid";
		               	document.getElementById("right" + first_ask_ix).style.borderTopWidth = "3px";
		               	document.getElementById("right" + first_ask_ix).style.borderTopColor = "red"; 		               	

		                for (var kx = parseInt(first_ask_ix); kx <= parseInt(last_ask_ix); kx++) {
		                	document.getElementById("ask" + kx.toString()).style.borderLeftStyle = "solid";
		                	document.getElementById("ask" + kx.toString()).style.borderLeftWidth = "3px";
		                	document.getElementById("ask" + kx.toString()).style.borderLeftColor = "red";

		                	document.getElementById("right" + kx.toString()).style.borderRightStyle = "solid";
		                	document.getElementById("right" + kx.toString()).style.borderRightWidth = "3px";
		                	document.getElementById("right" + kx.toString()).style.borderRightColor = "red";		                	
		                }

		                document.getElementById("ask" + last_ask_ix).style.borderBottomStyle = "solid";
		               	document.getElementById("ask" + last_ask_ix).style.borderBottomWidth = "3px";
		               	document.getElementById("ask" + last_ask_ix).style.borderBottomColor = "red"; 
		                document.getElementById("right" + last_ask_ix).style.borderBottomStyle = "solid";
		               	document.getElementById("right" + last_ask_ix).style.borderBottomWidth = "3px";
		               	document.getElementById("right" + last_ask_ix).style.borderBottomColor = "red"; 	               	       
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
		<table>		
		<tr>
			<th width="24%" style = "color:green"> Exchange </th>
			<th width="24%" style = "color:green"> Bid </th>
			<th width="2%"> </th>
			<th width="2%"> </th>
			<th width="24%" style = "color:red"> Ask </th>
			<th width="24%" style = "color:red"> Exchange </th>
		</tr>	
		<tr>
			<td id="left0">&nbsp;</td>
			<td id="bid0">&nbsp;</td>
			<td id="leftmid0">&nbsp;</td>
			<td id="rightmid0">&nbsp;</td>
			<td id="ask0">&nbsp;</td>
			<td id="right0">&nbsp;</td>
		</tr>
		<tr>
			<td id="left1">&nbsp;</td>
			<td id="bid1">&nbsp;</td>
			<td id="leftmid1">&nbsp;</td>
			<td id="rightmid1">&nbsp;</td>
			<td id="ask1">&nbsp;</td>
			<td id="right1">&nbsp;</td>
		</tr>
		<tr>
			<td id="left2">&nbsp;</td>
			<td id="bid2">&nbsp;</td>
			<td id="leftmid2">&nbsp;</td>
			<td id="rightmid2">&nbsp;</td>
			<td id="ask2">&nbsp;</td>
			<td id="right2">&nbsp;</td>
		</tr>
		<tr>
			<td id="left3">&nbsp;</td>
			<td id="bid3">&nbsp;</td>
			<td id="leftmid3">&nbsp;</td>
			<td id="rightmid3">&nbsp;</td>
			<td id="ask3">&nbsp;</td>
			<td id="right3">&nbsp;</td>
		</tr>
		<tr>
			<td id="left4">&nbsp;</td>
			<td id="bid4">&nbsp;</td>
			<td id="leftmid4">&nbsp;</td>
			<td id="rightmid4">&nbsp;</td>
			<td id="ask4">&nbsp;</td>
			<td id="right4">&nbsp;</td>
		</tr>
		<tr>
			<td id="left5">&nbsp;</td>
			<td id="bid5">&nbsp;</td>
			<td id="leftmid5">&nbsp;</td>
			<td id="rightmid5">&nbsp;</td>
			<td id="ask5">&nbsp;</td>
			<td id="right5">&nbsp;</td>
		</tr>
		<tr>
			<td id="left6">&nbsp;</td>
			<td id="bid6">&nbsp;</td>
			<td id="leftmid6">&nbsp;</td>
			<td id="rightmid6">&nbsp;</td>
			<td id="ask6">&nbsp;</td>
			<td id="right6">&nbsp;</td>
		</tr>
		<tr>
			<td id="left7">&nbsp;</td>
			<td id="bid7">&nbsp;</td>
			<td id="leftmid7">&nbsp;</td>
			<td id="rightmid7">&nbsp;</td>
			<td id="ask7">&nbsp;</td>
			<td id="right7">&nbsp;</td>
		</tr>
		<tr>
			<td id="left8">&nbsp;</td>
			<td id="bid8">&nbsp;</td>
			<td id="leftmid8">&nbsp;</td>
			<td id="rightmid8">&nbsp;</td>
			<td id="ask8">&nbsp;</td>
			<td id="right8">&nbsp;</td>
		</tr>
		<tr>
			<td id="left9">&nbsp;</td>
			<td id="bid9">&nbsp;</td>
			<td id="leftmid9">&nbsp;</td>
			<td id="rightmid9">&nbsp;</td>
			<td id="ask9">&nbsp;</td>
			<td id="right9">&nbsp;</td>
		</tr>
		<tr>
			<td id="left10">&nbsp;</td>
			<td id="bid10">&nbsp;</td>
			<td id="leftmid10">&nbsp;</td>
			<td id="rightmid10">&nbsp;</td>
			<td id="ask10">&nbsp;</td>
			<td id="right10">&nbsp;</td>
		</tr>
		<tr>
			<td id="left11">&nbsp;</td>
			<td id="bid11">&nbsp;</td>
			<td id="leftmid11">&nbsp;</td>
			<td id="rightmid11">&nbsp;</td>
			<td id="ask11">&nbsp;</td>
			<td id="right11">&nbsp;</td>
		</tr>	
		</table>
	</body>
	<button onclick="window.location.reload()"> Refresh Page </button>
	<!-- <input type="button" value="Refresh Page" onClick="window.location.reload()"> -->
</html>