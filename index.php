<?php
/*
* (c) 2016 Alex Mirtoff
* e-mail: alex@mirtoff.ru
* OOONETMAP
*
*/

session_start();

?>
<html>
<head>
    <title>Карта сети</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <script src="https://api-maps.yandex.ru/2.1/?lang=ru-RU" type="text/javascript"></script>
    <script src="https://yandex.st/jquery/2.1.0/jquery.min.js" type="text/javascript"></script>
    <script src="js/object_manager.js" type="text/javascript"></script>
	<style>
        html, body, #map {
            width: 100%; height: 100%; padding: 0; margin: 0;
        }
        .tst{ background-color: #474747;
            font-family: Helvetica;
            padding: 2px;
            text-align: center;
            font-size: 0.8em; 
            color: #FFD700;
            text-shadow: 0px 1px 1px #666;
        }
                                                                    
    </style>
</head>
<body>
<div class="tst">
Карта работает в режиме тестирования. Если не подгружаются связи, перезагрузите страницу (Объекты загружаются ~10 сек.)
</div>
<div id="map"></div>
</body>
</html>
