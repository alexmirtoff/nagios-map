<?php
/*
* (c) 2016 Alex Mirtoff
* e-mail: alex@mirtoff.ru
* OOONETMAP
* не используется
*
*/

function get_geo_pos($addr)
{

$stav_kray = "Ставропольский край+";
$response = json_decode(file_get_contents("https://geocode-maps.yandex.ru/1.x/?format=json&geocode='$stav_kray.$addr'"));
$to_return = $response->response->GeoObjectCollection->featureMember[0]->GeoObject->Point->pos;
return explode(" ", $to_return);

}

?>

