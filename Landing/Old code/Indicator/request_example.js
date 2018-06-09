var xhr = new XMLHttpRequest();

//xhr.open('GET', 'https://httpbin.org/ip', true); // test server

xhr.open('GET', 'https://api.exmo.com/v1/ticker/', true);
xhr.onload = function() {
  alert('Answer' + this.responseText);
}
xhr.onerror = function() {
  alert('Error ' + this.status);
}
xhr.send();
