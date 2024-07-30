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

if (!isset($_GET['searchTerm'])) {
    echo json_encode(['error' => 'No search term provided']);
    exit;
}

$searchTerm = $_GET['searchTerm'];
$data = [];

// Use prepared statements for security
$stmt = $conn->prepare("SELECT * FROM AldiItems_TEMP WHERE item_title LIKE CONCAT('%', ?, '%')");
$stmt->bind_param("s", $searchTerm);
$stmt->execute();
$result = $stmt->get_result();
while ($row = $result->fetch_assoc()) {
    $row['source'] = 'Aldi';
    $data[] = $row;
}
$stmt->close();

$stmt = $conn->prepare("SELECT * FROM SainsburysItems_TEMP WHERE item_title LIKE CONCAT('%', ?, '%')");
$stmt->bind_param("s", $searchTerm);
$stmt->execute();
$result = $stmt->get_result();
while ($row = $result->fetch_assoc()) {
    $row['source'] = 'Sainsburys';
    $data[] = $row;
}
$stmt->close();

echo json_encode($data);