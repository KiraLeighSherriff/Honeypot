<?php

require_once("dbConnect.php");

class AllPorts
{
    private $dbConn;

    // To get the database connection form the files
    public function __construct($dbConn)
    {
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

    public function PortPop(){
        try{
            $stmt = $this->dbConn->prepare("SELECT Port, COUNT(*) AS count FROM all_connect GROUP BY Port ORDER BY count DESC LIMIT 1;");
            $stmt->execute();
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            
            if ($result !== false) {
                $port = $result['Port'];
                echo $port;
            } 

        }
        catch (PDOException $e) {
           echo 'Command execution failed: ' . $e->getMessage();
        
        }
    }

    public function ClientIPPop(){
        try{
            $stmt = $this->dbConn->prepare("SELECT Client_ip, COUNT(*) AS count FROM all_connect GROUP BY Client_ip ORDER BY count DESC LIMIT 1;");
            $stmt->execute();
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            
            if ($result !== false) {
                $client_ip = $result['Client_ip'];
                echo $client_ip;
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
            $stmt = $this->dbConn->prepare("SELECT * FROM all_connect;");
            $stmt->execute(); # execute the command
            $result = $stmt->fetchAll(PDO::FETCH_ASSOC);  # Get the data within the table
                foreach ($result as $row) {
                    echo "<tr>
                        <td>".htmlspecialchars($row['ID'])."</td>
                        <td>".htmlspecialchars($row['Client_IP'])."</td>
                        <td>".htmlspecialchars($row['Port'])."</td>
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
$start = new AllPorts($dbConn);
$start->Session(); 

include('HTML/AllLogpage.html');
?>