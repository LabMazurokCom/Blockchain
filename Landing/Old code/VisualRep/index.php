<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>arbitrage indicator</title>
        <script>
            var 
                stockPrices,
                example, ctx,
                hCenter, drawHeight, drawWidth, barWidth, margin,
                bidBaseColor, ascBaseColor,
                bidStrokes, askStrokes,
                min, max, scaleKoeff;
            function get_rates()
            {
///start changes           	
                var xhr = new XMLHttpRequest();
                xhr.open('GET', 'rates.php', true);
                xhr.onload = function() 
                {
                  console.log("responseText= ",this.responseText);
                  var response = JSON.parse(this.responseText).list;
                  console.log("response=",response); 

///stop changes
        example = document.getElementById("example");
        ctx = example.getContext('2d');
	      drawHeight=example.height;
      	drawWidth=example.width;
      	barWidth=40;
      	margin=10;
      	hCenter=drawWidth/2;
        ctx.font = "12pt monospace";
        ctx.lineWidth = 1;
        var metrics = ctx.measureText('01234567890123456789');  //'10 - 7'
        var textBoxWidth=metrics.width;

			  DrawBorder();
      	DrawCenter();
      	stockPrices=GetStockPricesFromXHR(response);
        console.log(stockPrices);
        ScalePrices(stockPrices,drawHeight,margin);
        bidStrokes=GetBidStrokes(stockPrices);
        console.log(bidStrokes);
        var textHeight=14;  //must be real value !!!
        var bidYtop=drawHeight-bidStrokes.length*textHeight;
        var titleMargin=80;
        var bidXright=hCenter-titleMargin;
        ctx.textAlign="end";
   			//for (var i=bidStrokes.length-1; i>=0;i--)
        for (var i=0; i<bidStrokes.length;i++)
   			{
          var pretty=PrettyString(bidStrokes[i]['name'],bidStrokes[i]['srcPrice'],10,7);
     			ctx.fillText
     			(	pretty,
            //bidStrokes[i]['name']+' - '+bidStrokes[i]['srcPrice'],
            bidXright, 
            bidYtop+i*textHeight
            //drawHeight-margin-bidStrokes[i]['price']-2
          );
          //connect title with brick
          ctx.moveTo(bidXright, bidYtop+i*textHeight-textHeight/2);
          //ctx.lineTo(hCenter-barWidth, drawHeight-margin-bidStrokes[bidStrokes.length-i-1]['price']);
          ctx.lineTo(hCenter-barWidth, drawHeight-margin-bidStrokes[i]['price']);
          ctx.stroke();
			  }
      	askStrokes=GetAskStrokes(stockPrices);
        console.log(askStrokes);
        var askYtop=1;
        //var askXleft=drawWidth-textBoxWidth;  //must be more intelligent!
        var askXleft=hCenter+titleMargin;
        ctx.textAlign="left";
      	//for (var i=askStrokes.length-1;i>=0;i--)
        for (var i=0; i<bidStrokes.length;i++)
      	{
          var pretty=PrettyAskString(askStrokes[i]['name'],askStrokes[i]['srcPrice'],10,7);
     			ctx.fillText
     			(	pretty,
            //askStrokes[i]['name']+' - '+askStrokes[i]['srcPrice'],
            //hCenter+barWidth+10,
            askXleft,
            askYtop+(i+1)*textHeight
            //drawHeight-margin-askStrokes[i]['price']-2
          );
          //connect title with brick
          
          ctx.moveTo(askXleft, askYtop+i*textHeight+textHeight/2);
          //ctx.lineTo(hCenter+barWidth, drawHeight-margin-askStrokes[askStrokes.length-i-1]['price']);
          ctx.lineTo(hCenter+barWidth, drawHeight-margin-askStrokes[i]['price']);
          ctx.fillStyle = "rgb(150,150,150)";
          ctx.stroke();
          ctx.fillStyle = "rgb(0,0,0)";
   			}

   			StockBar(bidStrokes,hCenter-barWidth,drawHeight-margin,barWidth,'bid');
   			StockBar(askStrokes,hCenter,drawHeight-margin,barWidth,'ask');
        
        ctx.fillStyle = "rgb(100,100,110";
        DrawProfitPercent();
			}

/// start changes                
                xhr.onerror = function() { alert('Error ' + this.status); }
                xhr.send();
            }
///stop changes

///start cahges
            function GetStockPricesFromXHR(response)
            { 
            	//console.log(response);
                var stocks = [];
                //for (var x=0; x<response.length-1;i++)
                for (var x in response)
                {
                    console.log("x= ",x);
                    if ((response[x].bid!=0) &&(response[x].ask!=0))
                    stocks.push(
                    {   "name" : response[x].exchange,
                        "bid_top": response[x].bid,
                        "ask_top": response[x].ask
                    }
                    );
                }
                return stocks;
            }
///stop changes
      	function DrawBorder()
      	{
       		// ctx.moveTo(1,1);
       		// ctx.lineTo(drawWidth,1);
       		// ctx.lineTo(drawWidth,drawHeight);
       		// ctx.lineTo(1,drawHeight);
       		// ctx.stroke();
          ctx.fillStyle = "rgb(245,245,220)";
          ctx.fillRect( 1,1, drawWidth, drawHeight);
          ctx.fillStyle = "rgb(0,0,0)";
    		}
     		function DrawCenter()
     		{
       		ctx.moveTo(hCenter,0);
       		ctx.lineTo(hCenter,drawHeight);
       		ctx.stroke();
     		}
        function ScalePrices(stockPrices, drawHeight, margin)
        {
          min=stockPrices[0]['bid_top'];
          max=stockPrices[0]['ask_top'];
          for(var i=1;i<stockPrices.length;i++)
          {
            if(stockPrices[i]['bid_top']<min)
              min=stockPrices[i]['bid_top'];
            if(stockPrices[i]['ask_top']>max)
              max=stockPrices[i]['ask_top'];
            }
            scaleKoeff=(drawHeight-2*margin)/(max-min);
        }
     		function compareStockPrices(a, b)
     		{
       		if (a['price'] > b['price']) return -1;
       		if (a['price'] < b['price']) return 1;
     		}
     		function GetBidStrokes(stockPrices)
     		{
       		var scaledPrices=[];
       		for(var i=0;i<stockPrices.length;i++)
       		{
         		scaledPrices[i] =
       			{	name: stockPrices[i]['name'],
         			price : Math.round(scaleKoeff*(stockPrices[i]['bid_top']-min)),
         			srcPrice : stockPrices[i]['bid_top']
       			};
       		}
	        scaledPrices.sort(compareStockPrices);
       		return scaledPrices;
     		}
     		function GetAskStrokes(stockPrices)
     		{
       		var scaledPrices=[];
       		for(var i=0;i<stockPrices.length;i++)
       		{
            scaledPrices[i] =
     		    {	name: stockPrices[i]['name'],
         			price : Math.round(scaleKoeff*(stockPrices[i]['ask_top']-min)),
         			srcPrice : stockPrices[i]['ask_top']
       			};
       		}
       		scaledPrices.sort(compareStockPrices);
       		return scaledPrices;
     		}
     		function Profitable(bidStrokes,askStrokes)
     		{
       		if(bidStrokes[bidStrokes.length-1]['price']>askStrokes[0]['price'])
       			return true;
       		else
       			return false;
     		}
     		function ChangeAskColor(color)
     		{
     			if (color=="rgb(200,0,0)") return "rgb(255,0,0)";
     			else return "rgb(200,0,0)";
     		}
     		function ChangeBidColor(color)
     		{
     			if (color=="rgb(0,200,0)") return "rgb(0,255,0)";
     			else return "rgb(0,200,0)";
     		}
     		function StockBar(hStrokes,x,y,width, ttype)
     		{	var color;
          if (ttype=='ask') color= "rgb(200,0,0)";
         	if (ttype=='bid') color= "rgb(0,255,0)";
	        //strokes
	        for (var i=hStrokes.length-1; i>=0; i--)
       		{	ctx.moveTo(x, y-hStrokes[i]['price']);
         		ctx.lineTo(x+width, y-hStrokes[i]['price']);
         		ctx.stroke();
       		}
       		//bricks
       		for (var i=hStrokes.length-1; i>=1; i--)
       		{
       			ctx.fillStyle = color;
       			ctx.fillRect
       			(	x,
         			y-hStrokes[i]['price'],
         			width,
         			hStrokes[i]['price']-hStrokes[i-1]['price']
       			);
       			if (ttype=='bid') color=ChangeBidColor(color);
       			else color=ChangeAskColor(color);
	        }
          if (ttype=='ask')
          { ctx.fillStyle = color;
            ctx.fillRect
            ( x,
              0,
              width,
              margin
            );
          }
          else
          {
            ctx.fillStyle = color;
            ctx.fillRect
            ( x,
              drawHeight-margin,
              width,
              margin
            );
          }
       		//common border
       		ctx.moveTo(x,y-hStrokes[0]['price']);
       		ctx.lineTo(x+width,y-hStrokes[0]['price']);
	        ctx.lineTo(x+width,y-hStrokes[hStrokes.length-1]['price']);
       		ctx.lineTo(x,y-hStrokes[hStrokes.length-1]['price']);
	        ctx.lineTo(x,y-hStrokes[0]['price']);
       		ctx.stroke();
		    }
        function PrettyString(stockName, stockPrice, nameWidth, priceWidth)
        { 
          var part1=stockName;
          while (part1.length<nameWidth) {  part1=part1+' '; }
          var part2=stockPrice.toFixed(2);
          while (part2.length<priceWidth) {  part2=' '+part2; }
          return stockName+' - '+part2;
        }
        function PrettyAskString(stockName, stockPrice, nameWidth, priceWidth)
        { 
          var part1=stockName;
          while (part1.length<nameWidth) {  part1=part1+' '; }
          var part2=stockPrice.toFixed(2);
          while (part2.length<priceWidth) {  part2=' '+part2; }
          return part2+' - '+stockName;
        }
        function DrawProfitPercent()
        {
          //ctx.fillStyle = "rgb(255,255,255)";
          //ctx.fillRect( 1,1, 100, 100);

          var percent=
          (bidStrokes[0]['srcPrice']-askStrokes[askStrokes.length-1]['srcPrice'])
          /
          (bidStrokes[0]['srcPrice']+askStrokes[askStrokes.length-1]['srcPrice'])
          *200;
          percent=percent.toFixed(2);
          console.log(percent)*200;

          ctx.font = "24pt monospace";
          ctx.fillStyle="rgb(255,0,0)";
          ctx.fillText( percent+"%",20,25);
          ctx.fillStyle = "rgb(0,0,0)";
        }

        </script>
</head>
    <body onload="get_rates()">
        <canvas height='320' width='600' id='example'>Обновите браузер</canvas>
    </body>
</html>