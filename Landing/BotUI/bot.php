<?php
  $filename = './balances_post.txt';
  var_dump($_POST);
  if(!file_exists($filename)) {
    $filelink = fopen($filename, 'w');
  }
  else {
    $Filelink = fopen($filename, 'a');
  }
  fwrite($filelink, "data:".$_POST['json']."\n\n");
  fclose($filelink);
 ?>
