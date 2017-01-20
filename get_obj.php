<?php
/*
* (c) 2016 Alex Mirtoff
* e-mail: alex@mirtoff.ru
* OOONETMAP
*
*/
  session_start();
  $sess = session_id();
  $log_file = "./log/log.txt";
  $tmp_dir = "./tmp/";
  $tmp_json_file = "{$sess}.json";

 if (file_exists($tmp_dir . $tmp_json_file)) {
 	unlink($tmp_dir . $tmp_json_file);
 }
  

  $bbox = $_GET['bbox'];
  $callback = $_GET['callback'];
//$callback = "cb";
//  $range = "45.0170,41.9238,45.0365,41.9623";
  $range = $bbox;
  $out = $bbox . "\n";
  file_put_contents($log_file, $out, FILE_APPEND | LOCK_EX);
 
  $json_head = <<<EOD
{
 "type": "FeatureCollection",
         "features": [
EOD;

  $json_end = "]}"; 	     

/* work with DB */
function work_with_db($query) {

  $link = mysql_connect('localhost', '***', '****');
  mysql_set_charset('utf8', $link);
  if (!$link) {
        die('mysqlerror: ' . mysql_error());
  };
  mysql_select_db('netmap') or die('db use error');
  $result = mysql_query($query, $link) or die('fail' . mysql_error());
  mysql_close($link);
  return $result;
}


  $range_expl = explode(",", $range);
  $query_basic = "SELECT id, nag_hostname, nag_parent, info, 
	          ip_address, latitude, longitude, real_address, state, nag_parent_ip FROM new_geo WHERE latitude >= $range_expl[0] 
		  AND latitude <= $range_expl[2] AND longitude >= $range_expl[1] AND longitude <= $range_expl[3]";

/* get host range array from DB  */
  $hosts_array_basic = work_with_db($query_basic);
	
  $body = $json_head;

  while ($row_basic = mysql_fetch_assoc($hosts_array_basic))
  {
	  $body = $body . json_body($row_basic['id'], $row_basic['latitude'], $row_basic['longitude'], $row_basic['real_address'], 
		                    $row_basic['nag_hostname'], $row_basic['nag_parent'], $row_basic['ip_address'], $row_basic['info'], $row_basic['nag_parent_ip']);
	  if ($rows_count != mysql_num_rows($hosts_array_basic)-1){
		  $body = $body . ",\n";
	  }
	  $rows_count++;
  }


  $answ = $body . $json_end;

/* put answer to callback (JS) */ 
   if (file_exists($tmp_dir . $tmp_json_file)){
     unlink($tmp_dir . $tmp_json_file);
   }

  file_put_contents($tmp_dir . $tmp_json_file, $answ, FILE_APPEND | LOCK_EX);
  echo $callback . '('. $answ .')';

/* generate json body from template  */ 
function json_body($id, $latitude, $longitude, $real_address, $nag_hostname, $nag_parent, $ip_address, $info, $nag_parent_ip) {

  $body = <<<EOD
{"type":"Feature","id":{$id},"geometry":{"type":"Point","coordinates":["{$latitude}","{$longitude}"]},"properties":{"balloonContent":"Адрес: {$real_address}<br>IP: <a href='https://e.****.ru/reports/switch_status/?ip={$ip_address}' target='blank_'>{$ip_address}</a><br>Место установки: {$info}<br>Подключен от: <a href='https://e.***.ru/reports/switch_status/?ip={$nag_parent_ip}' target='blank_'>{$nag_parent} ($nag_parent_ip)</a>","clusterCaption":"{$nag_hostname} @ IP: {$ip_address}","hintContent":"{$real_address}"}}
EOD;


return $body;
}

?>
