<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>Arbitrage indicator</title>
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
                var xhr = new XMLHttpRequest();

                xhr.open('GET', 'rates.php', true);
                xhr.onload = function() 
                {
                    var response = JSON.parse(this.responseText).list;
                    stockPrices=GetStockPricesFromXHR(response);
                    example = document.getElementById("example");
                    ctx = example.getContext('2d');
                    drawHeight=example.height;
                    drawWidth=example.width;
                    barWidth=40;
                    margin=20;
                    hCenter=drawWidth/2;
                    DrawBorder();
                    DrawCenter();
                    ScalePrices(stockPrices,drawHeight,margin);
                    bidStrokes=GetBidStrokes(stockPrices);
                    for (var i=0; i<bidStrokes.length;i++)
                    {
                        var pretty=PrettyString(bidStrokes[i]['name'],bidStrokes[i]['srcPrice']);
                        console.log(pretty);
                        ctx.fillText
                        (   pretty,
                            //bidStrokes[i]['name']+' - '+bidStrokes[i]['srcPrice'],
                            hCenter-100,
                            drawHeight-margin-bidStrokes[i]['price']-2
                        );
                    }
                    askStrokes=GetAskStrokes(stockPrices);
                    for (var i=0; i<bidStrokes.length;i++)
                    {
                        var pretty=PrettyString(askStrokes[i]['name'],askStrokes[i]['srcPrice']);
                        ctx.fillText
                        (   pretty,
                            //askStrokes[i]['name']+' - '+askStrokes[i]['srcPrice'],
                            hCenter+barWidth+10,
                            drawHeight-margin-askStrokes[i]['price']-2
                        );
                    }
                    StockBar(bidStrokes,hCenter-barWidth,drawHeight-margin,barWidth,'bid');
                    StockBar(askStrokes,hCenter,drawHeight-margin,barWidth,'ask');
                }
                xhr.onerror = function() { alert('Error ' + this.status); }
                xhr.send();
            }
            function GetStockPricesFromXHR(response)
            { 
                var stocks = [];
                for (var x in response) 
                {
                    stocks.push(
                    {   "name" : response[x].exchange,
                        "bid_top": response[x].bid,
                        "ask_top": response[x].ask
                    }
                    );
                }
                return stocks;
            }
            function DrawBorder()
            {
                //ctx.fillStyle = "rgb(240,240,240)";
                //ctx.fillRect( 1,1,drawWidth,drawHeight );

                ctx.moveTo(1,1);
                ctx.lineTo(drawWidth,1);
                ctx.lineTo(drawWidth,drawHeight);
                ctx.lineTo(1,drawHeight);
                ctx.stroke(); 
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
                if (a['price'] > b['price']) return 1;
                if (a['price'] < b['price']) return -1;
            }
            function GetBidStrokes(stockPrices)
            {
                var scaledPrices=[];
                for(var i=0;i<stockPrices.length;i++)
                {
                    scaledPrices[i] =
                    {   name: stockPrices[i]['name'],
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
                    {   name: stockPrices[i]['name'],
                        price : Math.round(scaleKoeff*(stockPrices[i]['ask_top']-min)),
                        srcPrice : stockPrices[i]['ask_top']
                    };
                }
                scaledPrices.sort(compareStockPrices);
                return scaledPrices;
            }
            function ChangeBidColor(color)
            {
                if (color=="rgb(200,0,0)") return "rgb(255,0,0)";
                else return "rgb(200,0,0)";
            }
            function ChangeAskColor(color)
            {
                if (color=="rgb(0,200,0)") return "rgb(0,255,0)";
                else return "rgb(0,200,0)";
            }
            function StockBar(hStrokes,x,y,width, ttype)
            {   var color,titleOffset;
                if (ttype=='bid') 
                {
                    color= "rgb(200,0,0)";
                    titleOffset=-50;
                }
                if (ttype=='ask') 
                {
                    color= "rgb(0,255,0)";
                    titleOffset=100;
                }
                //strokes
                for (var i=hStrokes.length-1; i>=0; i--)
                {   ctx.moveTo(x+titleOffset, y-hStrokes[i]['price']);
                    ctx.lineTo(x+width, y-hStrokes[i]['price']);
                    ctx.stroke();
                }

                //bricks
                for (var i=hStrokes.length-1; i>=1; i--)
                {
                    ctx.fillStyle = color;
                    ctx.fillRect
                    (   x,
                        y-hStrokes[i]['price'],
                        width,
                        hStrokes[i]['price']-hStrokes[i-1]['price']
                    );
                    if (ttype=='bid') color=ChangeBidColor(color);
                    else color=ChangeAskColor(color);
                }
                //common border
                ctx.moveTo(x,y-hStrokes[0]['price']);
                ctx.lineTo(x+width,y-hStrokes[0]['price']);
                ctx.lineTo(x+width,y-hStrokes[hStrokes.length-1]['price']);
                ctx.lineTo(x,y-hStrokes[hStrokes.length-1]['price']);
                ctx.lineTo(x,y-hStrokes[0]['price']);
                ctx.stroke();
            }
            function PrettyString(stockName, stockPrice)
            { 
                var part1=stockName;
                while (part1.length<10) {  part1=part1+' '; }
                var part2=stockPrice.toFixed(2);
                while (part2.length<14) {  part2=' '+part2; }
                return part1+' - '+part2;
            }
        </script>
</head>
    <body onload="get_rates()">
        <canvas height='320' width='480' id='example'>Обновите браузер</canvas>
    </body>
</html>