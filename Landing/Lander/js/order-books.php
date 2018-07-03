<?php
//    Binance
  // error_reporting(0);
 $constants = file_get_contents('constants.json');
 $constants = json_decode($constants);
 $address = $constants -> address;

 $options  = array("http" => array("user_agent" => "curl/7.29.0"));
 $context  = stream_context_create($options);

 for($i = 0; $i < count($address); $i ++) {
   try {
     $x = file_get_contents($address[$i], false, $context);
     echo $x;
     echo '<br></br>';
   } catch(Exception $e) {
     echo $e;
   }
 }
?>
