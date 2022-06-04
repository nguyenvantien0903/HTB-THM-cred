<?php
include "auth_check.php";
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <title>Simple WebApp</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="./css/bootstrap.min.css">
    <script src="./js/jquery.min.js"></script>
    <script src="./js/bootstrap.min.js"></script>

    <style>
        html, body {
            margin: 0;
            padding: 0;
            max-width: 100%;
            overflow-x: hidden;
        }

    </style>

</head>
<body>

<nav class="navbar navbar-default">
    <div class="container-fluid">
        <div class="navbar-header">
            <a class="navbar-brand" href="#">Simple WebApp</a>
        </div>
        <ul class="nav navbar-nav">
            <?php
            if (isset($_SESSION['userid'])) {
            ?>
            <li><a href="index.php">Home</a></li>
            <li class=""><a href="profile.php">Edit profile</a></li>

            <?php
            if (isset($_SESSION['role']) && $_SESSION['role'] == 1) {
                ?>
                <li><a href="avatar_uploader.php">Admin panel</a></li>

            <?php }
            ?>


        </ul>
        <ul class="nav navbar-nav navbar-right">
            <li><a href="logout.php">Logout</a></li>

            <?php
            } else {

                ?>
                <li><a href="login.php">Login</a></li>
                <?php

            }
            ?>
        </ul>
    </div>
</nav>
