<?php

require_once("dbConnect.php");


class Settings
{
    private $user_account;

    private $dbConn;

    public function __construct($dbConn)
    {
        // To open the connection form the other files
        $this->dbConn = $dbConn;

        $json_file = file_get_contents("username.json");
        $json_data = json_decode($json_file, true);
        // get the username of windows form the json file for script termination 
        $this->user_account = $json_data['username']['user'];
    }

     // If user in not logged in redirect to login page
    public function Session(){

        if(!isset($_SESSION)) { 
            session_start(); 
       } 

        // Session time out after 10 minutes 
       if (isset($_SESSION['LAST_ACTIVITY']) && (time() - $_SESSION['LAST_ACTIVITY']) > 600) {
            session_unset();
            session_destroy();
        }
        
        $_SESSION['LAST_ACTIVITY'] = time();

        if (!(isset($_SESSION['user_id']) && $_SESSION['user_id'] != '')) {
            header("Location: login.php");
            exit();
        }
        
    }

    // Open all the file between 0-1024, this includes all the developed ports
    public function OpenAllControl(){
        // get the windows username
        $current_user = $this->user_account;

        // create the cookie
        $all_cookie = isset($_COOKIE['opencookie']) && $_COOKIE['opencookie'] == 'on' ? 'checked' : '';

        // get the pid form the launch files to execute the script if needed
        $json_file = file_get_contents("C:\\Users\\{$current_user}\\Honeypot\\LaunchFiles\\pids.json");
        $json_data = json_decode($json_file, true);
        $main_pid = $json_data['pythonpid']['allpid'];

        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            // set the cookie to store the status of the ticked box
            $open_all = isset($_POST['OpenAll']) ? $_POST['OpenAll'] : 'off';
            setcookie("opencookie", $open_all, time()+3600);
            $all_cookie = $open_all == 'on' ? 'checked': '' ;

            // if the check of is ticked launch file
            if($all_cookie == 'checked'){

                // if the pid is -1 start else dont
                if ($main_pid == -1){
                     // start in background execute command, place to store the output, stops hanging
                    $command = 'start /b python.exe "C:\Users\\'.$current_user.'\\Honeypot\\LaunchFiles\\LaunchAll.py" > log1.txt 2>&1';
                    pclose(popen($command, 'r')); // open and close pipe for the command to be executed
                }
                
            }
            elseif($main_pid != '-1'){
                    // terminate the proccess 
                    exec("taskkill /PID $main_pid /F");
                    /* Update JSON file with -1 once terminated, this is done just in case a program running with the pid store in the JSON file while the
                    file is not loaded. This could cause the termination of an innocent program the user might want to be terminated. */
                    $json_data['pythonpid']['allpid'] = -1;
                    $json_object = json_encode($json_data, JSON_PRETTY_PRINT); // Make the JSON file look good
                    file_put_contents("C:\\Users\\{$current_user}\\Honeypot\\LaunchFiles\\pids.json", $json_object);
                }
            }
            
        return $all_cookie;
    }

    // Open ssh launch file
    public function SSHControl(){
        $current_user = $this->user_account;

        $ssh_cookie = isset($_COOKIE['sshcookie']) && $_COOKIE['sshcookie'] == 'on' ? 'checked' : '';

        $json_file = file_get_contents("C:\\Users\\{$current_user}\\Honeypot\\LaunchFiles\\pids.json");
        $json_data = json_decode($json_file, true);
        $ssh_pid = $json_data['pythonpid']['sshpid'];

        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $open_ssh = isset($_POST['SSHOpen']) ? $_POST['SSHOpen'] : 'off';
            setcookie("sshcookie", $open_ssh, time()+3600);
            $ssh_cookie = $open_ssh == 'on' ? 'checked' : '';

            if ($ssh_cookie == 'checked'){
                if ($ssh_pid == -1){
                    $command = 'start /b python.exe "C:\Users\\'.$current_user.'\\Honeypot\\LaunchFiles\\LaunchSSH.py" > log2.txt 2>&1';
                    pclose(popen($command, 'r')); 
                }
            }
            elseif($ssh_pid != '-1'){
                // terminate the proccess 
                exec("taskkill /PID $ssh_pid /F");
                $json_data['pythonpid']['sshpid'] = -1;
                $json_object = json_encode($json_data, JSON_PRETTY_PRINT);
                file_put_contents("C:\\Users\\{$current_user}\\Honeypot\\LaunchFiles\\pids.json", $json_object);
                }
            }

        return $ssh_cookie;
    }


    public function TelnetControl(){
        $current_user = $this->user_account;

        $telnet_cookie = isset($_COOKIE['telnetcookie']) && $_COOKIE['telnetcookie'] == 'on' ? 'checked' : '';

        $json_file = file_get_contents("C:\\Users\\{$current_user}\\Honeypot\\LaunchFiles\\pids.json");
        $json_data = json_decode($json_file, true);
        $telnet_pid = $json_data['pythonpid']['telnetpid'];

        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $open_telnet = isset($_POST['TelnetOpen']) ? $_POST['TelnetOpen'] : 'off';
            setcookie("telnetcookie", $open_telnet, time()+3600);
            $telnet_cookie = $open_telnet == 'on' ? 'checked' : '';
        
            if ($telnet_cookie == 'checked'){
                if ($telnet_pid == -1){
                    $command = 'start /b python.exe "C:\Users\\'.$current_user.'\\Honeypot\\LaunchFiles\\LaunchTelnet.py" > log3.txt 2>&1';
                    pclose(popen($command, 'r'));
                }
            }
            elseif($telnet_pid != '-1'){ 
                    exec("taskkill /PID $telnet_pid /F");
                    $json_data['pythonpid']['telnetpid'] = -1;
                    $json_object = json_encode($json_data, JSON_PRETTY_PRINT);
                    file_put_contents("C:\\Users\\{$current_user}\\Honeypot\\LaunchFiles\\pids.json", $json_object);
            }

        }
        return $telnet_cookie;
    }


    public function FTPControl(){
        $current_user = $this->user_account;
    
        $ftp_cookie = isset($_COOKIE['ftpcookie']) && $_COOKIE['ftpcookie'] == 'on' ? 'checked' : '';

        $json_file = file_get_contents("C:\\Users\\{$current_user}\\Honeypot\\LaunchFiles\\pids.json");
        $json_data = json_decode($json_file, true);
        $ftp_pid = $json_data['pythonpid']['ftppid'];

        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $open_ftp = isset($_POST['FTPOpen']) ? $_POST['FTPOpen'] : 'off';
            setcookie("ftpcookie", $open_ftp, time()+3600);
            $ftp_cookie = $open_ftp == 'on' ? 'checked' : '';

            if ($ftp_cookie == 'checked'){
                if($ftp_pid == -1){
                    $command = 'start /b python.exe "C:\Users\\'.$current_user.'\\Honeypot\\LaunchFiles\\LaunchFTP.py" > log4.txt 2>&1';
                    pclose(popen($command, 'r')); 
                }
            }
            elseif($ftp_pid != '-1'){
                    exec("taskkill /PID $ftp_pid /F");
                    $json_data['pythonpid']['ftppid'] = -1;
                    $json_object = json_encode($json_data, JSON_PRETTY_PRINT);
                    file_put_contents("C:\\Users\\{$current_user}\\Honeypot\\LaunchFiles\\pids.json", $json_object);
                }

        }
         return $ftp_cookie;
    }

    public function HTTPControl(){
        $current_user = $this->user_account;

        $http_cookie = isset($_COOKIE['httpcookie']) && $_COOKIE['httpcookie'] == 'on' ? 'checked' : '';

        $json_file = file_get_contents("C:\\Users\\{$current_user}\\Honeypot\\LaunchFiles\\pids.json");
        $json_data = json_decode($json_file, true);
        $http_pid = $json_data['pythonpid']['httppid'];

        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $open_http = isset($_POST['HTTPOpen']) ? $_POST['HTTPOpen'] : 'off';
            setcookie("httpcookie", $open_http, time()+3600);
            $http_cookie = $open_http == 'on' ? 'checked' : '';

            if ($http_cookie == 'checked'){
                if($http_pid == -1){
                    $command = 'start /b python.exe "C:\Users\\'.$current_user.'\\Honeypot\\LaunchFiles\\LaunchHTTP.py" > log5.txt 2>&1';
                    pclose(popen($command, 'r'));
                }
            }

            elseif($http_pid != '-1'){
                    exec("taskkill /PID $http_pid /F");
                    $json_data['pythonpid']['httppid'] = -1;
                    $json_object = json_encode($json_data, JSON_PRETTY_PRINT);
                    file_put_contents("C:\\Users\\{$current_user}\\Honeypot\\LaunchFiles\\pids.json", $json_object);
            }

        }
        return $http_cookie;
    }

    public function DownloadDatabase(){
        $current_user = $this->user_account;
 
        if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["Download"]) && $_POST["Download"] == "Download") {
            $command = 'start /b python.exe C:\\Users\\'.$current_user.'\\Honeypot\\Database\\DownloadDatabase.py';
            pclose(popen($command, 'r'));
        }

    }

    // Call a python file that will flush the database, by deleting all tables then recreating them
    public function FlushDatabase(){
        $current_user = $this->user_account;

        if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["Flush"]) && $_POST["Flush"] == "Flush") {
            $command = 'start /b python.exe C:\\Users\\'.$current_user.'\\Honeypot\\Database\\FlushDatabase.py';
            pclose(popen($command, 'r'));
        }

    }


/* This part of the code will modify the json files that control the login for the database and the protocol my allow the user to
    modify the JSON file that store the information. All of this code is very similar only different is the file path and variable names  */

    // Get the data from the form and sent it the the function to be processed 
    public function GetInfo(){
        if ($_SERVER["REQUEST_METHOD"] == "POST") {

            // Get the data form the web application so it can be used to modify the backend JSON files
            $db_host = $_POST['db_host'] ?? ''; 
            $db_port = $_POST['db_port'] ?? '';
            $db_user = $_POST['db_user'] ?? '';
            $db_passwd = $_POST['db_passwd'] ?? '';

            # get the email form post
            $email = $_POST['Email'] ?? '';

            # get ssh creds form post
            $ssh_username = $_POST['ssh_username'] ?? ''; 
            $ssh_password = $_POST['ssh_password'] ?? '';

            # get telnet cred for post
            $telnet_username= $_POST['telnet_username'] ?? '';
            $telnet_password = $_POST['telnet_password'] ?? '';

            // Call the functions that are going to be used to change the values in the JSON
            $this-> ChangeDatabaseInfo($db_host, $db_port, $db_user, $db_passwd);
            $this->ChangeEmail($email);
            $this-> ChangeSSHCreds($ssh_username, $ssh_password);
            $this-> ChangTelnetCreds($telnet_username, $telnet_password);
        }
    }

    // Change the database information for the user login 
    public function ChangeDatabaseInfo($db_host, $db_port, $db_user, $db_passwd){
        $current_user = $this->user_account;
 
        // Get teh JSON file that contain this information 
        $json_file = file_get_contents("C:\\Users\\{$current_user}\\Honeypot\\Database\\Config\\db_config.json");
        $json_data = json_decode($json_file, true);

        // If the input provided by the user is not empty then update the JSON File
        if (!empty($db_host)){
            $json_data['database_config']['db_host'] = $db_host;
            $json_object = json_encode($json_data, JSON_PRETTY_PRINT); // Ensure that the JSON file is in a easy to read formate
            file_put_contents("C:\\Users\\{$current_user}\\Honeypot\\Database\\Config\\db_config.json", $json_object); // path to json file
        }

        if (!empty($db_port)){
            $json_data['database_config']['db_port'] = $db_port;
            $json_object = json_encode($json_data, JSON_PRETTY_PRINT);
            file_put_contents("C:\\Users\\{$current_user}\\Honeypot\\Database\\Config\\db_config.json", $json_object);
        }

        if (!empty($db_user)){
            $json_data['database_config']['db_user'] = $db_user;
            $json_object = json_encode($json_data, JSON_PRETTY_PRINT);
            file_put_contents("C:\\Users\\{$current_user}\\Honeypot\\Database\\Config\\db_config.json", $json_object);
        }

        if (!empty($db_passwd)){
            $json_data['database_config']['db_passwd'] = $db_passwd;
            $json_object = json_encode($json_data, JSON_PRETTY_PRINT);
            file_put_contents("C:\\Users\\{$current_user}\\Honeypot\\Database\\Config\\db_config.json", $json_object);
        }

    }

    // Change the email address that allow the program to sends alerts
    public function ChangeEmail($email){
        $current_user = $this->user_account;

        $json_file = file_get_contents("C:\\Users\\{$current_user}\\Honeypot\\Alert\\\Email.json"); // paht to file
        $json_data = json_decode($json_file, true);

        // ensure it is an email that has been entered
        if(!filter_var($email, FILTER_VALIDATE_EMAIL) & !empty($email)) {
            $error = "<h3>Warring Invalid email format<h3>";
            echo $error;
          }

        
        if (!empty($email)){
            // sent post form data into json file
            $json_data['EmailAddress']['user_email'] = $email;
            $json_object = json_encode($json_data, JSON_PRETTY_PRINT);
            file_put_contents("C:\\Users\\{$current_user}\\Honeypot\\Alert\\\Email.json", $json_object);
        }
    }


    // Change the SSH creds that allow teh user to login 
    public function ChangeSSHCreds($ssh_username, $ssh_password){
        $current_user = $this->user_account;

        $json_file = file_get_contents("C:\\Users\\{$current_user}\\Honeypot\\Protocols\\SSH\\creds.json");
        $json_data = json_decode($json_file, true);
        
        if (!empty($ssh_username)){
            $json_data['ssh_login']['ssh_username'] = $ssh_username;
            $json_object = json_encode($json_data, JSON_PRETTY_PRINT);
            file_put_contents("C:\\Users\\{$current_user}\\Honeypot\\Protocols\\SSH\\creds.json", $json_object);
        }

        if (!empty($ssh_password)){
            $json_data['ssh_login']['ssh_password'] = $ssh_password;
            $json_object = json_encode($json_data, JSON_PRETTY_PRINT);
            file_put_contents("C:\\Users\\{$current_user}\\Honeypot\\Protocols\\SSH\\creds.json", $json_object);
        }
    }


    // Change the creds of telnet protocols
    public function ChangTelnetCreds($telnet_username, $telnet_password){
        $current_user = $this->user_account;
      
        $json_file = file_get_contents("C:\\Users\\{$current_user}\\Honeypot\\Protocols\\Telnet\\creds.json");
        $json_data = json_decode($json_file, true);

        
        if (!empty($telnet_username)){
            $json_data['telnet_login']['telnet_username'] = $telnet_username;
            $json_object = json_encode($json_data, JSON_PRETTY_PRINT);
            file_put_contents("C:\\Users\\{$current_user}\\Honeypot\\Protocols\\Telnet\\creds.json", $json_object);
        
        }

        if (!empty($telnet_password)){
            $json_data['telnet_login']['telnet_password'] = $telnet_password;
            $json_object = json_encode($json_data, JSON_PRETTY_PRINT);
            file_put_contents("C:\\Users\\{$current_user}\\Honeypot\\Protocols\\Telnet\\creds.json", $json_object);
        }
    }
}

// instantiate  the class
$start= new Settings($dbConn);
$start->Session();
$start->GetInfo();

// call the functions
$flush = $start->FlushDatabase();
$Download = $start->DownloadDatabase();
$all= $start->OpenAllControl();
$ssh = $start->SSHControl();
$telnet = $start->TelnetControl(); 
$ftp = $start->FTPControl();
$http = $start->HTTPControl();
include ('HTML/settings.html');
?>
