<?php

require_once("dbConnect.php");
class Home
{
    private $dbConn;

    public function __construct($dbConn)
    {
        // To open the connection form the other files
        $this->dbConn = $dbConn;
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


    // Get the top 10  most popular ports that have been accessed as a summary
    public function PortPop(){
        try{
            // sql command to  get hte most common ports by a limit of 10
            $stmt = $this->dbConn->prepare("SELECT Port, COUNT(*) AS count FROM all_connect GROUP BY Port ORDER BY count DESC LIMIT 10;");
            $stmt->execute(); // execute commmadn
            $result = $stmt->fetchAll(PDO::FETCH_ASSOC); // get data form the results
            foreach ($result as $row) { 
                // ehco to html
                echo "<tr>
                    <td>".htmlspecialchars($row['Port'])."</td>
                    <td>".htmlspecialchars($row['count'])."</td>
                </tr>";
            }
            echo "</table>";

        }
        // catch erro
        catch (PDOException $e) {
            echo 'Command execution failed: ' . $e->getMessage();
        }
    }      

    // Get the top 10 IP addressed that have accessed the honeypot
    public function ClientIPPop(){
        try{
            $stmt = $this->dbConn->prepare("SELECT Client_IP, COUNT(*) AS count FROM all_connect GROUP BY Client_IP ORDER BY count DESC LIMIT 10;");
            $stmt->execute();
            $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
            foreach ($result as $row) {
                echo "<tr>
                    <td>".htmlspecialchars($row['Client_IP'])."</td>
                    <td>".htmlspecialchars($row['count'])."</td>
                </tr>";
            }
            echo "</table>";
        }
        catch (PDOException $e) {
           echo 'Command execution failed: ' . $e->getMessage();
        
        }
    }

    // SSH logins for the home page
    public function Usernamessh(){
        try{
            $stmt = $this->dbConn->prepare("SELECT Username, COUNT(*) AS count FROM ssh_login GROUP BY Username ORDER BY count DESC LIMIT 1;");
            $stmt->execute();
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            
            if ($result !== false) {
                $username = $result['Username'];
                echo $username;
            } 

        }
        catch (PDOException $e) {
           echo 'Command execution failed: ' . $e->getMessage();
        
        }
    }

    public function Passwordssh(){
        try{
            $stmt = $this->dbConn->prepare("SELECT password, COUNT(*) AS count FROM ssh_login GROUP BY password ORDER BY count DESC LIMIT 1;");
            $stmt->execute();
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            
            if ($result !== false) {
                $password = $result['password'];
                echo $password;
            } 

        }
        catch (PDOException $e) {
           echo 'Command execution failed: ' . $e->getMessage();
        
        }
    }

    // Telnet logins for the home page
    public function Usernametelnet(){
        try{
            $stmt = $this->dbConn->prepare("SELECT Username, COUNT(*) AS count FROM telnet_login GROUP BY Username ORDER BY count DESC LIMIT 1;");
            $stmt->execute();
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            
            if ($result !== false) {
                $username = $result['Username'];
                echo $username;
            } 

        }
        catch (PDOException $e) {
           echo 'Command execution failed: ' . $e->getMessage();
        
        }
    }

    public function Passwordtelnet(){
        try{
            $stmt = $this->dbConn->prepare("SELECT password, COUNT(*) AS count FROM telnet_login GROUP BY password ORDER BY count DESC LIMIT 1;");
            $stmt->execute();
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            
            if ($result !== false) {
                $password = $result['password'];
                echo $password;
            } 

        }
        catch (PDOException $e) {
           echo 'Command execution failed: ' . $e->getMessage();
        
        }
    }

    //http login for the home page
    public function Usernamehttp(){
        try{
            $stmt = $this->dbConn->prepare("SELECT Username, COUNT(*) AS count FROM http_login GROUP BY Username ORDER BY count DESC LIMIT 1;");
            $stmt->execute();
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            
            if ($result !== false) {
                $username = $result['Username'];
                echo $username;
            } 

        }
        catch (PDOException $e) {
           echo 'Command execution failed: ' . $e->getMessage();
        
        }
    }

    public function Passwordhttp(){
        try{
            $stmt = $this->dbConn->prepare("SELECT password, COUNT(*) AS count FROM http_login GROUP BY password ORDER BY count DESC LIMIT 1;");
            $stmt->execute();
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            
            if ($result !== false) {
                $password = $result['password'];
                echo $password;
            } 

        }
        catch (PDOException $e) {
           echo 'Command execution failed: ' . $e->getMessage();
        
        }
    }

    // ftp logins for the home page 
    public function Usernameftp(){
        try{
            $stmt = $this->dbConn->prepare("SELECT Username, COUNT(*) AS count FROM ftp_login GROUP BY Username ORDER BY count DESC LIMIT 1;");
            $stmt->execute();
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            
            if ($result !== false) {
                $username = $result['Username'];
                echo $username;
            } 
        }
        catch (PDOException $e) {
           echo 'Command execution failed: ' . $e->getMessage();
        
        }
    }

    public function Passwordftp(){
        try{
            $stmt = $this->dbConn->prepare("SELECT password, COUNT(*) AS count FROM ftp_login GROUP BY password ORDER BY count DESC LIMIT 1;");
            $stmt->execute();
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            
            if ($result !== false) {
                $password = $result['password'];
                echo $password;
            } 

        }
        catch (PDOException $e) {
           echo 'Command execution failed: ' . $e->getMessage();
        
        }
    }
}


$start= new Home($dbConn);
$start->Session(); 
include ('HTML/homepage.html');
?>
