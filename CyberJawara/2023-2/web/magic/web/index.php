<?php
include('recaptcha.php');
include('magic.php');
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <title>Magic!</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        form {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        input[type="file"] {
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 4px;
            width: calc(100% - 22px);
        }

        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 10px;
        }

        button:hover {
            background-color: #45a049;
        }
    </style>
    <script src="https://www.google.com/recaptcha/api.js" async defer></script>
</head>
<body>
    <form action="index.php" method="post" enctype="multipart/form-data">
        <div class="g-recaptcha" data-sitekey="6LfmVSMpAAAAAGNELwUw0qSfoniwb_RVFTsbn2D9"></div>
        <input type="file" name="image" required>
        <button type="submit">Upload</button>
        <?php
            if ($resizedImagePath) {
                echo '<p><img src="' . htmlentities($resizedImagePath) . '"></img></p>';
            } else if ($error) {
                echo '<p>' . htmlentities($error) . '</p>';
            }
        ?>
    </form>
</body>
</html>