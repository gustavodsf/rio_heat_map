<?php
	$type = trim($_POST['type']);
	if($type=='kde'){
		exec('python3.4 cgi-bin/kde.py', $dataFromPython);
		//echo($dataFromPython);
		echo(empty($dataFromPython)) ? "python não carregou" : json_encode($dataFromPython);
	}
	else{
		exec('python3.4 cgi-bin/machine_learning.py', $dataFromPython);
		//echo($dataFromPython);
		echo(empty($dataFromPython)) ? "python não carregou" : json_encode($dataFromPython);	
	}
?>