function readFromServer(address, callback) {

  function reqListener() {
    callback(this.responseText);
  }

  let xhr = new XMLHttpRequest();
  xhr.addEventListener('load', reqListener);
  xhr.open('GET', address);
  xhr.send();
}

function go() {
  readFromServer('http://192.168.15.74:5000/get_pairs', function(text) {
    console.log(text);
  })
}
