<?php
    $servername = "dbhost.cs.man.ac.uk"; 
    $username = "n61969aa"; 
    $password = "62Whitfield"; 
    $databasename = "2023_comp10120_z8";

    $conn = mysqli_connect($servername, $username, $password, $databaseName);

    $un = $_POST['username'];
    $pw = $_POST['password'];
    // print $pass . "_" . $email;

    $query = mysqli_query($conn, "SELECT log_username,log_password FROM login WHERE log_username='$un' AND log_password='$pw'");

    $result_can = mysqli_query($conn, $query);

    if (mysqli_num_rows($result_can) > 0) {
        echo "Login Successful";
        //redirect to home page
        header("Location: ../new_homepage.html");
        exit;
    } else {
        echo "Login Failed";
        //redirect to login page
        header("Location: ../login_page.html");
        exit;
    }
    mysqli_close($conn);
?>

