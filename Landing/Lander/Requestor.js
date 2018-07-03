function Requester(_config) {
  let config = _config;

  this.setConfig = function(_config) {
    config = _config;
  }

  this.sendRequest = function(exchange, params) {
    let request_string = this.getRequestString(exchange, params);
    let result = {};
    readFromServer(request_string, function(text) {
      result = this.processResponce(JSON.parse(text));
    })
    return result;
  }

  this.getRequestString = getRequestString;
  this.sendRequestsToExchanges = sendRequestsToExchanges;
  this.processResponce = processResponce;
  this.runProcess = runProcess;
  return this;
}


function sendRequestsToExchanges(params) {
  let responce = {};
  for (let exchange in config) {
    let address = this.getRequestString(exchange, params);
    readFromServer(address, function(text) {
      let rsp = JSON.parse(text);
      responce[exchange] = rsp;
    })
  }
  return responce;
}


function getEntityFromPath(object, path, currency_pair) {
  let link = object;
  for (let i = 0; i < path.length; i++) {
    if (path[i] === "{}") path[i] = config['converter'][currency_pair];
    link = link[path[i]];
  }
  return link;
}

/*
Мне нужно слить все найденные биды и аски в один список бидов и в одим список асков
После этого мне нужно отсортировать биды по убыванию, маски по возрастанию
*/
function processResponce(responce, params) {
  let asks = [];
  let bids = [];

  for (let exchange in responce) {
    // let conf = config[exchange];
    price_ptr = config[exchange]['fields']['price'];
    volume_ptr = config[exchange]['fields']['volume'];

    let path = config[exchange]['path']['bids'];
    let bid = getEntityFromPath(responce[exchange], path, params[
      'currency_pair']);

    path = config[exchange]['path']['asks'];
    let ask = getEntityFromPath(responce[exchange], path, params[
      'currency_pair']);

    for (let order of bid) {
      bids.add({
        price: order[price_ptr],
        volume: order[volume_ptr],
        exchange: exchange
      });
    }

    for (let order of ask) {
      asks.add({
        price: order[price_ptr],
        volume: order[volume_ptr],
        exchange: exchange
      });
    }
  }

  bids.sort((a, b) => a.price - b.price);
  asks.sort((a, b) => b.price - a.price);

  return [bids, asks];
}


function processResponceData(bids, asks, d) {
  bids_count = bids.length;
  asks_count = asks.length:


}


function runProcess(params) {
  let responce = this.sendRequestsToExchanges(params);
  let [bids, asks] = this.processResponce(responce, params);
  return this.processResponceData(bids, asks);
}


function getRequestString(echange, params) {
  /*
  params = {
    currency_pair: btc_usd,
    some_paramater: boolean_value
  }
  */
  let currency_pair = config[exchange]['converter'][params['currency_pair']];
  return formatObj(config[exchange]['url'], [currency_pair]);
}


function readFromServer(address, callback) {

  function reqListener() {
    callback(this.responseText);
  }

  let xhr = new XMLHttpRequest();
  xhr.addEventListener('load', reqListener);
  xhr.open('GET', address);
  xhr.send();
}


function formatObj(str, dict) {
  let res = str.slice();
  console.log("i am in format");
  for (let key in dict) {
    res = res.replace(new RegExp('(\\{' + key + '\\})', 'g'), dict[key]);
  }
  return res;
}
