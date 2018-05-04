
const template = `
<div class="main main-content arbitrage arbitrage-container" style="padding-top: 40px;">
<table>
  <tr>
  <td>
      <!-- table with extra bids and asks -->
    <table id = "table0{0}">
      <tr>
        <td colspan="5">
          <div class="panel-heading">
            <div class="table_title container cust_container">
              <div> <span>BTC/USD</span> </div>
              <div> <span id = "time">{1}</span></div>
            </div>
          </div>
        </td>
      </tr>
      <tr>
        <td style ="width:20%"><h4 class="arbitrage-head">Highest bid price</h4></td>
        <td style ="width:20%"><h4 class="arbitrage-head">Lowest ask price</h4></td>
        <td style ="width:20%"><h4 class="arbitrage-head">Percentage</h4></td>
        <td style ="width:20%"><h4 class="arbitrage-head">Maximum volume</h4></td>
        <td style ="width:20%"><h4 class="arbitrage-head">Profit</h4></td>
      </tr>
      <tr>
        <td style ="width:20%"><div class="arbitrage-price" id = "max_bid{0}">{2}</div></td>
        <td style ="width:20%"><div class="arbitrage-price" id = "min_ask{0}">{3}</div></td>
        <td style ="width:20%"><div class="arbitrage-price" id = "percent{0}">{4}</div></td>
        <td style ="width:20%"><div class="arbitrage-price" id = "volume{0}">{5}</div></td>
        <td style ="width:20%"><div class="arbitrage-price" id = "profit{0}">{6}</div></td>

      </tr>

    </table>
    <table id = "table1{0}">
      <tr>
        <td id = "ask_col" style = "background-color:#ffe1e6;width:50%" class="arbitrage-info-text alert">
          <p id = "ask_col_p" style = "text-align:left;font-size:60%">{7}</p>
        </td>
        <td id = "bid_col" style = "width:50%" class="arbitrage-info-text alert">
          <p id = "bid_col_p" style = "text-align:left;font-size:60%">{8}</p>
        </td>
      </tr>
    </table>

      <!-- orders -->

  </td>
  <td>
    <div >
      <img id="jpg-export{0}"></img>
    </div>

  </td>
</tr>
</table>

</div>`

function genTable(obj) {
  return formatObj(template, obj);
}

function formatObj(str, dict) {
  let res = str.slice();
  console.log("i am in format");
  for(let key in dict) {
    console.log(key, ('{'+key+'}').match(new RegExp('(\\{'+ key + '\\})', 'g')));
    res = res.replace(new RegExp('(\\{'+ key + '\\})', 'g'), dict[key]);
  }
  return res;
}

function showticker(id, data) {

  var maxbid = 0;
  var minask = 29 * 1e13;
  var max_bid_exchange = "";
  var min_ask_exchange = "";

  for (var i = 0; i < data["ticker"].length; i++) {
    if (maxbid < data["ticker"][i]["bid"]) {
      maxbid = +data["ticker"][i]["bid"];
      max_bid_exchange = data["ticker"][i]["exchange"];
    }
    if (minask > data["ticker"][i]["ask"]) {
      minask = +data["ticker"][i]["ask"];
      min_ask_exchange = data["ticker"][i]["exchange"];
    }
  }

  let cur_time = new Date();
  maxbid = maxbid.toFixed(2);
  minask = minask.toFixed(2);
  percent = ((maxbid - minask) / maxbid * 100).toFixed(2)
  volume = data["amount"].toFixed(2);
  profit = data['profit'].toFixed(2);

  var ask_orders = "";
  var bid_orders = "";
  console.log(data["orders"]);
  var n = Object.keys(data["orders"]["asks"]).length;
  var i = 0;
  for (var exch in data["orders"]["asks"]) {
    ask_orders += "Buy " + (+data["orders"]["asks"][exch][1]).toFixed(8) +
      " BTC for a price of " + (+data["orders"]["asks"][exch][0]).toFixed(2) +
      " USD at " + exch;

    if (i < n - 1) ask_orders += "<br>";
    i++;
  }

  var n = Object.keys(data["orders"]["bids"]).length;
  var i = 0;
  for (var exch in data["orders"]["bids"]) {
    bid_orders += "Sell " + (+data["orders"]["bids"][exch][1]).toFixed(8) +
      " BTC for a price of " + (+data["orders"]["bids"][exch][0]).toFixed(2) +
      " USD at " + exch;
    if (i < n - 1) bid_orders += "<br>";
    i++;
  }

  console.log(ask_orders);
  console.log(bid_orders);

  //create build vector
  res_array = [
    id,
    cur_time,
    maxbid,
    minask,
    percent,
    volume,
    profit,
    ask_orders,
    bid_orders
  ];

  document.getElementById('exch' + id).innerHTML = genTable(res_array);

  res_obj = {
    'id' : id,
    'cur_time' : cur_time,
    'maxbid' : maxbid,
    'minask' : minask,
    'percent' : percent,
    'volume' : volume,
    'profit' : profit,
    'ask_orders' : ask_orders,
    'bid_orders' : bid_orders
  };
  //Ploting
  var d3 = Plotly.d3;
  var img_jpg = d3.select("#jpg-export" + id);

  var myPlot = document.getElementById("plot");
  x = data["amount_points"];
  y = data["profit_points"];
  // console.log(x);
  // console.log("\n\n\n")
  // console.log(y);
  // console.log(data.optimal_point)
  data = [{
    x: x,
    y: y,
    type: "scatter",
    mode: "lines+markers",
  }, {
    x: [data.optimal_point.amount],
    y: [data.optimal_point.profit],
    type: "scatter",
    marker: {
      color: "red",
      size: 10
    }
  }];
  layout = {
    // title: "Profit vs Amount",
    // titlefont:{
    // 	size:14
    // },
    // autosize: true,
    // autoscale: true,
    margin: {
      l: 50,
      b: 50,
      t: 5,
      r: 20
    },
    title: false,
    width: 300,
    height: 300,
    xaxis: {
      title: "Amount, USD",
      titlefont: {
        size: 10
      },
      tickfont: {
        size: 7
      }
    },
    yaxis: {
      title: "Profit, USD",
      titlefont: {
        size: 10
      },
      tickfont: {
        size: 7
      }
    },
    showlegend: false
  };

  try {
    Plotly.deleteTraces(plot, [-2, -1]);
  } catch (e) {}
  Plotly.plot("plot", data, layout).then(
    function(gd) {
      return Plotly.toImage(gd, {
        format: "svg",
        height: 150,
        width: 300
      }).then(
        function(url) {
          img_jpg.attr("src", url);
        }
      )
    });

}

function readFromServer(address, callback) {

  function reqListener() {
    callback(this.responseText);
  }
  var xhr = new XMLHttpRequest();
  xhr.addEventListener('load', reqListener);
  xhr.open('GET',
    'https://arbitrage-logger.firebaseio.com/log_btc_usd.json?orderBy=%22$key%22&limitToLast=1&print=pretty'
  );
  xhr.send();
}

function update() {
  file = './read_from_firebase.php';
  address =
    'https://arbitrage-logger.firebaseio.com/log_btc_usd.json?orderBy=%22$key%22&limitToLast=1'
  try {
    readFromServer(address, function(text) {

      var data = JSON.parse(text);
      console.log(data);
      showticker(0, data[Object.keys(data)[0]]);
      showticker(1, data[Object.keys(data)[0]]);
      showticker(2, data[Object.keys(data)[0]]);

    });
  } catch (e) {
    console.log('here we have failed');
  }
}
