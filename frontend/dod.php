<?php 
header('Content-Type: application/json');

$servername = "dbhost.cs.man.ac.uk"; 
$username = "n61969aa"; 
$password = "62Whitfield"; 
$databasename = "2023_comp10120_z8";

// Create connection
$conn = new mysqli($servername, $username, $password, $databasename);

// Check connection
if ($conn->connect_error) {
    echo json_encode(['error' => 'Database connection failed: ' . $conn->connect_error]);
    exit;
}

//get everything from the table
$data = [];
$stmt = $conn->prepare("SELECT * FROM DOD_List");
$stmt->execute();
$result = $stmt->get_result();

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}
$stmt->close();

echo json_encode($data);
?>



