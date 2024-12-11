<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Watt Monster</title>
    <link rel="icon" type="image/x-icon" href="images/favicon.ico">
    <link rel="stylesheet" href="css/style.css">
    <script src="js/script.js"></script>
    <script src="js/jquery-3.7.1.min.js"></script>
</head>
<body>

<?php
$load_file = '';
if (isset($_GET['month']) && isset($_GET['year'])) {
    $month = (int)$_GET['month'];
    $year = (int)$_GET['year'];
    $file_glob = './generated/watt_monster_'. $year .'_' . sprintf('%02d', $month) . '_*.html';
    $result_file_list = glob($file_glob);
    if (count($result_file_list) == 1) {
        $load_file = $result_file_list[0];
    }
} ?>

<!--
<div style="border: 1px solid black; background-color:rgb(250,250,250); border-radius:10px;   box-shadow: 4px 4px lightgray; padding: 10px; width:60%;">
    <h3>(Watt-)Monster of the Month</h3>
    Given that people may join this group at random points in the
    season it seems unfair to have them linger at the end of the league table forever, so here's
    a new feature: the "(Watt-)Monster of the Month" competition, a mini-league table extracted from all the races in a
    given month. Now you can experience the end-of-season madness every month. Yay!
</div>
-->

<div>
    <h1>Rvy Racing: Watt Monster</h1>
    <?php
    if ($load_file != '') {
        readfile($load_file);
    }
    else {
        echo '<h1>No Watt-Monster found</h1>';
    }
    ?>
</div>
</body>
</html>
