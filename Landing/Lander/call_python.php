<?php
  $FILE_CHANGE_TIME = 5;
  $PATH_TO_DIR = '/var/www/mazurok.com/lab/'; //"/Library/WebServer/Documents/Lander/"
  $PATH_TO_INTERPRETER = '/usr/bin/python3'; //"/Users/deniskartashov/anaconda3/bin/python"
  $PATH_TO_DIR = "/Library/WebServer/Documents/Lander/";
  $PATH_TO_INTERPRETER = "/Users/deniskartashov/anaconda3/bin/python";
  $SEMAPHORS_DIR = 'sem';


  function init($SEMAPHORS_DIR) {
    if(!file_exists($SEMAPHORS_DIR)){
      $oldmask = umask(0);  // helpful when used in linux server
      mkdir ($SEMAPHORS_DIR, 0744);
    }
  }

  function get_sem($symbol) {
    $filename = "sem/".$symbol.'sem.txt';
    $sem = fopen($filename, 'w');
    echo 'sem '.$symbol.' created';
    return $sem;
  }

  function is_sem($symbol) {
    $filename = "sem/".$symbol.'sem.txt';
    return file_exists($filename);
  }

  function del_sem($symbol, $sem) {

    $filename = "sem/".$symbol.'sem.txt';
    fclose($sem);
    unlink($filename);
    echo 'sem '.$symbol.' deleted';

  }

  $commands = array(
    "btc_usd" => $PATH_TO_INTERPRETER." ".$PATH_TO_DIR."logger_with_fee.py btc_usd 10",
    "eth_usd" => $PATH_TO_INTERPRETER." ".$PATH_TO_DIR."logger_with_fee.py eth_usd 10",
    "xrp_usd" => $PATH_TO_INTERPRETER." ".$PATH_TO_DIR."logger_with_fee.py xrp_usd 10"
  );

  // var_dump($commands);

  init($SEMAPHORS_DIR);
  if(empty($_GET)) {
    foreach($commands as $key => $value) {
      $filename = $PATH_TO_DIR.$key.'.json';
      var_dump($filename);

      if(time() - filemtime($filename) < $FILE_CHANGE_TIME) {
        sleep($FILE_CHANGE_TIME - time() + filemtime($filename));
      }

      if(time() - filemtime($filename) > $FILE_CHANGE_TIME && !is_sem($key)) {
        $sem = get_sem($key);
        exec($value, $out, $status);
        var_dump($out);
        var_dump($status);
        del_sem($key, $sem);
      }
      else {
        sleep(2);
        echo "PHP: $key Access is blocked";
      }
    }
  }
  else {
    $symbol = $_GET['symbol'];
    $filename = $PATH_TO_DIR.$symbol.'.json';

    if(time() - filemtime($filename) < $FILE_CHANGE_TIME) {
      sleep($FILE_CHANGE_TIME - time() + filemtime($filename));
    }

    if(time() - filemtime($filename) > $FILE_CHANGE_TIME && !is_sem($symbol)) {
      $sem = get_sem($symbol);
      exec($commands[$symbol], $out, $status);
      var_dump($out);
      var_dump($status);
      del_sem($symbol, $sem);
    }
    else {
      sleep(2);
      echo "PHP: $symbol Access is blocked";
    }
  }
?>
