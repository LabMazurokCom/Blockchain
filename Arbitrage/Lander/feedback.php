<?php


  $email_to = "lab@mazurok.com";
  $email_subject = $_POST['subject'];
  try {
    $email_header = $_POST['email'];
  } catch (Exception $e) {
      header('Location:mail-error.html');
      exit();
  }
  if(empty($email_header)) {
    header('Location:mail-error.html');
    exit();
  }
  try {
      $email_body = $_POST['message'];
  } catch (Exception $e) {
      $email_body = "I have nothing to say";
  }


  if(mail($email_to, $email_subject, $email_body, $email_header)){
      header('Location:mail-success.html');

  } else {
        header('Location:mail-error.html');
  }

 ?>
