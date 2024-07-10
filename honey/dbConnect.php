<?php

    $json_file = file_get_contents("username.json");
    $json_data = json_decode($json_file, true);
    $user_account = $json_data['username']['user'];
    $json_file = file_get_contents("C:\\Users\\{$user_account}\\Honeypot\\Database\\Config\\db_config.json");

    $json_data = json_decode($json_file, true);

    /* Get Database information for JSON to be used 
        to make a connection */
    $db_host = $json_data['database_config']['db_host'];
    $db_user = $json_data['database_config']['db_user'];
    $db_port = $json_data['database_config']['db_port'];
    $db_passwd = $json_data['database_config']['db_passwd'];
    $db_name = $json_data['database_config']['db_name'];

    // Connect to the database and catch errors
    // Using PDO for database connection for error handling
    try {
        $dbConn = new PDO("mysql:host=$db_host;port=$db_port;dbname=$db_name", $db_user, $db_passwd);
        $dbConn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $dbConn->query("USE honeypot;");
    } catch (PDOException $e) {
        echo 'Connection failed: ' . $e->getMessage();
    }

?>