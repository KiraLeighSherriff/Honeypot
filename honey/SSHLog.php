<?php

require_once("dbConnect.php");

class SSHLogins
{
    private $dbConn;

    // To get the database connection form the files
    public function __construct($dbConn)
    {
        $this->dbConn = $dbConn;
    }

    // If user in not logged in redirect to login page
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

    // most common username entered
    public function UsernamePop(){
        try{
            $stmt = $this->dbConn->prepare("SELECT Username, COUNT(*) AS count FROM ssh_login GROUP BY Username ORDER BY count DESC LIMIT 1;");
            $stmt->execute();
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            
            if ($result !== false) {
                $username = $result['Username'];
                echo $username;
            } 
            else {
                echo "";
            }
        }
        catch (PDOException $e) {
           echo 'Command execution failed: ' . $e->getMessage();
        
        }
    }

    // most common passsword entered 
    public function PasswordPop(){
        try{
            $stmt = $this->dbConn->prepare("SELECT password, COUNT(*) AS count FROM ssh_login GROUP BY password ORDER BY count DESC LIMIT 1;");
            $stmt->execute();
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            
            if ($result !== false) {
                $password = $result['password'];
                echo $password;
            } 
            else {
                echo "";
            }
        }
        catch (PDOException $e) {
           echo 'Command execution failed: ' . $e->getMessage();
        
        }
    }

    // Function to view the data with on the files
    public function ViewData(){

        try {
            // Getting data from the tables to display in the html file
            $stmt = $this->dbConn->prepare("SELECT * from ssh_login");
            $stmt->execute(); # execute the command
            $result = $stmt->fetchAll(PDO::FETCH_ASSOC);  # Get the data within the table
                foreach ($result as $row) {
                    echo "<tr>
                        <td>".htmlspecialchars($row['ID'])."</td>
                        <td>".htmlspecialchars($row['Username'])."</td>
                        <td>".htmlspecialchars($row['Password'])."</td>
                        <td>".htmlspecialchars($row['Date'])."</td>
                        <td>".htmlspecialchars($row['Time'])."</td>
                    </tr>";
                }
                echo "</table>";
            }
         catch (PDOException $e) {
            echo 'Command execution failed: ' . $e->getMessage();
        }
    }

}


$start= new SSHLogins($dbConn);
$start->Session(); 

include('HTML/sshlogs.html');
?>