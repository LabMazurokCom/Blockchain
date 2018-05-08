<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Arbitrage opportunities</title>
    <script type="text/javascript" src="./js/jquery.min.js">
    </script>
    <script type="text/javascript" src="./js/jquery-ui.min.js">
    </script>
    <script type="text/javascript" src="./js/popper.min.js">
    </script>
    <script src="./js/bootstrap.min.js">
    </script>
    <script src="./js/jquery.dataTables.1.10.16.min.js">
    </script>
    <script type="text/javascript" src="./js/main.js">
    </script>
    <script type="text/javascript" src="./js/main-search.js">
    </script>
    <script src="https://www.gstatic.com/firebasejs/4.13.0/firebase.js">
    </script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js">
    </script>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="apple-touch-icon" sizes="180x180" href="./img/favicons/apple-touch-icon.png"/>
    <link rel="icon" type="image/png" sizes="32x32" href="./img/favicons/favicon-32x32.png"/>
    <link rel="icon" type="image/png" sizes="16x16" href="./img/favicons/favicon-16x16.png"/>
    <link rel="manifest" href="./img/favicons/manifest.json"/>
    <link rel="mask-icon" href="./img/favicons/safari-pinned-tab.svg" color="#5bbad5"/>
    <link rel="shortcut icon" href="./img/favicons/favicon.ico"/>
    <meta name="msapplication-config" content="./img/favicons/browserconfig.xml"/>
    <meta name="theme-color" content="#ffffff"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <meta name="google" content="notranslate"/>
    <meta http-equiv="Content-Language" content="en"/>
    <meta name="description" content="Arbitrage opportunities for trading cryptocurrencies by buying at one exchange and selling on another" />
    <link rel="stylesheet" type="text/css" href="./css/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="./css/jquery.dataTables.min.css"/>
    <link rel="stylesheet" type="text/css" href="./css/jquery-ui.min.css"/>
    <link rel="stylesheet" type="text/css" href="./css/informers.css/">
      <link rel="stylesheet" type="text/css" href="./css/denisStyles.css"/>
      <!-- <link rel="stylesheet" type="text/css" href="css/nv.d3.min.css" />		 -->
      <link rel="stylesheet" type="text/css" href="./css/responsive.css" />
      <link rel="stylesheet" type="text/css" href="./css/styles.css" />
      <!-- <link rel="stylesheet" type="text/css" href="css/form2.css" />		 -->
      <link rel="stylesheet" href="./css/font-awesome.min.css"/>
      <link href="/css/fonts.googleapis.com.montserrat.100.900.css" rel="stylesheet"/>
      <link rel="stylesheet" href="/css/hidden_panel.css">
      <!-- <script type="text/javascript" src="js/smallCharts.js">
    </script> -->
    <script type="text/javascript" src="generate.js">
    </script>
  </head>
  <body onload = 'update();setInterval(update, 5000);' >

    <!-- <input type="checkbox" id="hmt" class="hidden-menu-ticker">

    <label class="btn-menu" for="hmt">
      <span class="first"></span>
      <span class="second"></span>
      <span class="third"></span>
    </label>

    <ul class="hidden-menu">
      <li><a href="">Link 1</a></li>
      <li><a href="">Link 2</a></li>
      <li><a href="">Link 3</a></li>
    </ul> -->
    <!-- <div class="informer" style = 'width:200;height:300;background:red_bg'>      I am here and you can't do anything with it    </div> -->
    <div class="main main-content arbitrage arbitrage-container" style="padding-top: 40px;">
      <div id = 'exch0'>
      </div>
      <div id = 'exch1'>
      </div>
      <div id = 'exch2'>
      </div>
      <div id = 'exch3'>
      </div>
      <div id = 'exch4'>
      </div>
      <div id = 'exch5'>
      </div>
      <div id = 'exch6'>
      </div>
      <div id = 'exch7'>
      </div>
      <div id = 'exch8'>
      </div>
      <div id = 'plot' style="display:none;">
      </div>
    </div>
  </body>
</html>