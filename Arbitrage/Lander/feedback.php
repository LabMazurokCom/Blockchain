<?php


  $email_to = "lab@mazurok.com";
  $email_subject = "Please, contact me";
  $email_body = "I wan't to ask you about your work";
  mail($email_to, $email_subject, $email_body);
  // var_dump($_POST);
  if(mail($email_to, $email_subject, $email_body)){
      header('Location:mail-success.html');

  } else {
      header('Location:mail-error.html');
  }
// require_once("./include/fgcontactform.php");
//
// $formproc = new FGContactForm();
//
// //1. Add your email address here.
// //You can add more than one recipients.
// $formproc->AddRecipient('yourname@your-website.com'); //<<---Put your
//                                                           //email address here
//
// //2. For better security. Get a random string from
// // this link: http://tinyurl.com/randstr
// // and put it here
// $formproc->SetFormRandomKey('gkEFthfv6gvGAuL');
//
// if(isset($_POST['submitted']))
// {
//    if($formproc->ProcessForm())
//    {
//         $formproc->RedirectToURL("index.html");
//    }
// }

 ?>
