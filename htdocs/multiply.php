<?php
$error = "Invalid input";
$ans = "";
if (isset($_POST['num1']) && isset($_POST['num2'])) {
    $num1 = $_POST['num1'];
    $num2 = $_POST['num2'];

    $error = "";

    // check if the numbers are valid
    if (!is_numeric($num1) || !is_numeric($num2))
        $error = "Invalid input";
    else
        $ans = $num1 * $num2;
}

?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Simple Web Server</title>
    <link rel="stylesheet" href="./style.css">
</head>

<body>

    <div class="form-wrapper">
        <div class="form">
            <div class="error"><?php echo $error; ?></div>
            <?php
            if ($error == "")
                echo "The answer is: " . $ans;
            ?>
            <br />
            <a href="./">Back</a>
        </div>
    </div>

</body>

</html>