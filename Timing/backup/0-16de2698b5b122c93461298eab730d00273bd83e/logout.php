<?php

include "auth_check.php";

session_destroy();

echo "Logout successful";
header("Location: ./login.php");
