<script type="text/javascript">

function readTextFile(file, callback) {
  var result = null;
  var rawFile = new XMLHttpRequest();
  rawFile.overrideMimeType("application/json");
  rawFile.onreadystatechange = function() {
      if (rawFile.readyState === 4 && rawFile.status == "200") {
        callback(rawFile.responseText);
      }
  }
  rawFile.open("GET", file, true);

  rawFile.send(null);
}




function showticker(data) {
  var maxbid = 0;
  var minask = 29 * 1e13;
  var max_bid_exchange = '';
  var min_ask_exchange = '';
  console.log(data['ticker'])
  for(var i = 0 ; i < data['ticker'].length; i++) {
    if(maxbid < data['ticker'][i]['bid']) {
      maxbid = data['ticker'][i]['bid'];
      max_bid_exchange = data['ticker'][i]['exchange'];
    }
    if(minask > data['ticker'][i]['ask']) {
      minask = data['ticker'][i]['ask'];
      min_ask_exchange = data['ticker'][i]['exchange'];
    }
  }
  percent = (((maxbid-minask) / maxbid * 100).toFixed(2))
  console.log(maxbid, minask, percent);
  var divs = document.createElement('div');
  divs.innerHtml = '<div class="arbitrage-row">' +
            '<div class="panel-heading">' +
              '<div class="table_title container cust_container">' +
              '<div>Trade <span>BTC/EUR</span> from <span>kraken</span> to <span>lakebtc</span></div>'+
              '<div>Cryptocoin BTC/EUR arbitrage opportunity seen at <span>15:10 April 26th 2018</span></div>'+
            '</div>'+
          '</div>'+
          '<div class="container cust_container">'+
            '<div class="panel panel-default">'+
              '<div class="panel-body">'+
                '<div class="row">'+
                  '<div class="col-md-3">'+
                    '<h4 class="arbitrage-head">Highest bid price</h4>'+

                    '<div class="arbitrage-price">' + maxbid + '</div>'+
                  '</div>'+
                  '<div class="col-md-3">'+
                    '<h4 class="arbitrage-head">Lowest ask price</h4>'+
                    '<div class="arbitrage-price">' + minask + '</div>'+
                  '</div>'+
                  '<div class="col-md-3">'+
                    '<h4 class="arbitrage-head"> Percentage </h4>'+

                    '<div class="arbitrage-price">' + percent + '% </div>'+
                  '</div>'+
                  '<div class="col-md-3">'+
                    '<h4 class="arbitrage-head">Maximum volume</h4>'+
                    '<div class="arbitrage-price">' + data['amount'] + '</div>'+
                  '</div>'+
                '</div>'+
              '</div>'+
              '<p class="arbitrage-info-text alert">'+
              'You can <span>buy 0.0006 BTC for a price of 7307.60000000 EUR</span> at'+
              'kraken and <span>sell it for a price of 7682.00000000 EUR</span> at'+
              'lakebtc. This will make you a <span>profit of 0.22464 EUR</span>!'+
              '</p>'+
            '</div>' +
          '</div>' +
        '</div>';

}

function update() {
  file = 'example.json'
  readTextFile(file, function(text){

      var data = JSON.parse(text);
      console.log(data);
      showticker(data);

  });
}
</script>
