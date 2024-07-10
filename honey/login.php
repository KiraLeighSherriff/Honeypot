<?php


require_once("dbConnect.php");

class WebLogin
{
    private $dbConn;

    public function __construct($dbConn)
    {
        // To open the connection form the other files
        $this->dbConn = $dbConn;
        if(!isset($_SESSION)) { 
            session_start(); 
        }
    }


    /* This is done so the user can fist login with any information in the database
    once the use has login in the cred used will be store in the database. Then will 
    not be used again till not cred found in web_account table. */
    public function CheckTable()
    {
        // prepare mysql statement to get amount of accounts 
        try {
            $stmt = $this->dbConn->prepare("SELECT COUNT(*) as count FROM web_account");
            $stmt->execute();
            $count = $stmt->fetch(PDO::FETCH_ASSOC)['count'];
        } 
        catch (PDOException $e) {
            echo 'Command execution failed: ' . $e->getMessage();
        }

        // If not data in table sent to Register to make a account
        if($count == 0 ){
            $this->Register();
        }
        else{
            $this->LoginPage();
        }
    }

    // Register accounts 
    public function Register(){
        // To dynamically change the page information 
        $title = "<h1> Register </h1>";
        $info = "";
        $error_username = "";
        $error_password = "";
     
        // If method is po meaning if the web app is getting data from the client
        if ($_SERVER["REQUEST_METHOD"] == "POST") {

            // Get the username and password
            $username = $_POST['username'] ?? ''; 
            $password = $_POST['password'] ?? '';

                // Error if both or 1 is empty for security reasons
                if (empty($username) || empty($password)) {
                    // Alter the page
                    $info = "<p1>Username and Password Required</p1>";
                    return [$info, $title, include('HTML/login.html')];
                }
                else{
                    // Sanitize the data remove characters below ASCII 32
                    $sanitized_username= filter_input(INPUT_POST,'username',FILTER_SANITIZE_SPECIAL_CHARS);
                    $sanitized_password= filter_input(INPUT_POST,'password',FILTER_SANITIZE_SPECIAL_CHARS);
                    $password_length = strlen($sanitized_password);


                        // To check if the user has put in the incorrect symbols 
                        if ($sanitized_username !== $username || $sanitized_password !== $password ){
                            // Sent message of error
                            $error_password = "<p1>  *Use of illegal Characters</p1>";
                            return [$error_password, $title, include('HTML/login.html')];
                        }
                        // password should be more then 8 character
                        elseif($password_length <= 8){
                            $error_password = "<p1>  *Password Should be more then 8 characters</p1>";
                            return [$error_password, $title, include('HTML/login.html')];
                        }
                        // No symbols in username
                        elseif(!ctype_alnum($sanitized_username) ){
                            $error_username = "<p1> *Username Should only contain Characters & Numbers </p1>";
                            return [$error_username, $title, include('HTML/login.html')];
                        }
                        // password should contain a digit
                        elseif(!preg_match("/\d/", $sanitized_password)) {
                            $error_password = "<p1>  *Should contain at least one digit</p1>";
                            return [$error_password, $title, include('HTML/login.html')];
                        }
                        // password should contain a symbol 
                        elseif(!preg_match("/\W/", $sanitized_password)) {
                            $error_password = "<p1> *Should contain at least one Special Character</p1>";
                            return [$error_password, $title, include('HTML/login.html')];
                        }
                        else {
                            // Hash the password with bcrypt then put it into the database
                            $hashed_password = password_hash($password, PASSWORD_DEFAULT);
                            // preparing MySQL command for database 
                            try{
                                $stmt = $this->dbConn->prepare("INSERT INTO web_account (Username, password) VALUES (:username, :password)");
                                $stmt->bindParam(':username', $username, PDO::PARAM_STR);
                                $stmt->bindParam(':password', $hashed_password);
                            } catch (PDOException $e) {
                                echo 'Command execution failed: ' . $e->getMessage();
                            }
                            $stmt->execute(); // input the data to the database 
                            header("Location: login.php"); // send the user to the login page so they can make a session for login
                        }
                }                  
        }
        include('HTML/login.html');
    }   

    public function LoginPage()
    {
            // To send information to say no username and password
            $title = "<h1> Honeypot Login </h1>";
            $info = "";
            $error_username = "";
            $error_password = "";
            

            if ($_SERVER["REQUEST_METHOD"] == "POST") {

            // Get the username and password
            $username = $_POST['username'] ?? ''; 
            $password = $_POST['password'] ?? '';

                // Error if both or 1 is empty for security reasons
                if (empty($username) || empty($password)) {
                    // Alter the page
                    $info = "<p1>Username and Password Required</p1>";
                }
                else{
                    // Sanitize the data remove characters below ASCII 32, to prevent SQL injections
                    $sanitized_username = filter_input(INPUT_POST,'username',FILTER_SANITIZE_SPECIAL_CHARS);
                    $sanitized_password = filter_input(INPUT_POST,'password',FILTER_SANITIZE_SPECIAL_CHARS);

                        // To check if the user has put in the incorrect symbols 
                        if ($sanitized_username !== $username || $sanitized_password !== $password) {
                            // Sent message of error
                            $info = "<p1> Invalid Credentials </p1>";
                            return [$info, $title, include('HTML/login.html')];
                            // stop process
                        }
                        else {
                            try{
                                $stmt = $this->dbConn->prepare("SELECT * FROM web_account WHERE username =:username"); // Mysql statement 
                                $stmt->bindParam(':username', $username, PDO::PARAM_STR); // To specify teh variable name in Sql statement
                                $stmt->execute(); // input the data to the database 
                                $result = $stmt->fetch(PDO::FETCH_ASSOC); // fetch the Row associated with the username
                            } catch (PDOException $e) {
                                echo 'Command execution failed: ' . $e->getMessage();
                            }

                            /* This was added due to a bool error if the username was wrong but the password was correct
                                sql uses username to get info if username is incorrect password will be null, pass very dont like null values */
                            if (!isset($result['password'])) { // Extract password form the FETCH_ACCOS
                                $info = "<p1>Incorrect Credentials</p1>"; 
                                return [$info, $title, include('HTML/login.html')]; // Redirects user to login page to try again
                            }
                            
                            /* Verify to check if the hash values matched. */
                            if (password_verify($password, $result['password'])) {
                                header("Location: index.php"); // send the user to the home page 
                                $_SESSION['user_id'] = $result['ID']; // Start the session with a successful login
                            }
                            else{
                                $info = "<p1>Incorrect Credentials</p1>"; // If credentials where wrong
                            }
                        }
                }                  
        }
        include('HTML/login.html');
    }   
}

// Create an instance of the Login class
$start= new WebLogin($dbConn);
$start->CheckTable(); 

?>