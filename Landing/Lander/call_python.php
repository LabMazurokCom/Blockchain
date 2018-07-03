<?php
  $commands = array(
    "btc_usd" => "/usr/bin/python3 /var/www/mazurok.com/lab/logger_with_fee.py btc_usd 10",
    "eth_usd" => "/usr/bin/python3 /var/www/mazurok.com/lab/logger_with_fee.py eth_usd 10",
    "xrp_usd" => "/usr/bin/python3 /var/www/mazurok.com/lab/logger_with_fee.py xrp_usd 10"
  );

  var_dump($_GET);

  if(empty($_GET)) {
    foreach($commands as $value) {
      exec($value, $out, $status);
      var_dump($out);
      var_dump($status);
    }
  }
  else {
    exec($commands[$_GET['symbol']], $out, $status);
    var_dump($out);
    var_dump($status);
  }
?>
