<?php
/*
* (c) 2016 Alex Mirtoff
* e-mail: alex@mirtoff.ru
* OOONETMAP
*
*/
 

 if (isset($_POST['values'])) $req_parent = $_POST['values'] or die("error");
//$req_parent = [1, 2 ,3];
 // if (file_exists('log/from_js')) unlink("log/from_js");

 $link = mysql_connect('localhost', '***', '****');
 mysql_set_charset('utf8', $link);
 if (!$link) {
     die('mysqlerror: ' . mysql_error());
			      };
 mysql_select_db('netmap') or die('db use error');

 $out = implode(',', $req_parent) . "\n";
 file_put_contents('log/from_js', $out, FILE_APPEND);

 $query_polyline = "SELECT t2.nag_hostname_full, t2.latitude, t2.longitude, t1.nag_hostname_full AS parent,
			  t1.latitude AS parent_latitude, t1.longitude AS parent_longitude FROM new_geo AS t1 JOIN new_geo AS t2 ON 
			  t1.nag_hostname_full = t2.nag_parent WHERE t2.id IN(" . implode(',',$req_parent). ")";
 $result = mysql_query($query_polyline, $link) or die('fail' . mysql_error());
 
 
 while ($row = mysql_fetch_assoc($result)) {
    $export_array[] = ['latitude' => $row['latitude'], 'longitude' => $row['longitude'], 
	              'parent_latitude' => $row['parent_latitude'], 'parent_longitude' => $row['parent_longitude']];
 }

 mysql_close($link);

 $json_out_array = json_encode($export_array);
 
 //print_r($json_out_array);
 echo $json_out_array;


?>

