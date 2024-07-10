<?php

require_once("dbConnect.php");

class SSHCommand
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

    public function ViewData(){
        
        try {
            // Getting data from the tables to display in the html file
            $stmt = $this->dbConn->prepare("SELECT * from ssh_command");
            $stmt->execute(); # execute the command
            $result = $stmt->fetchAll(PDO::FETCH_ASSOC);  # Get the data within the table
                foreach ($result as $row) {
                    echo "<tr>
                        <td>".htmlspecialchars($row['ID'])."</td>
                        <td>".htmlspecialchars($row['Date'])."</td>
                        <td>".htmlspecialchars($row['Time'])."</td>
                        <td>".htmlspecialchars($row['Command'])."</td>
                    </tr>";
                }
                echo "</table>";
            }
         catch (PDOException $e) {
            echo 'Command execution failed: ' . $e->getMessage();
        }

    }
}

$start= new SSHCommand($dbConn);
$start->Session(); 
include ('HTML/sshcommands.html');

$start->ViewData();
?>
