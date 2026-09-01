<?php
header('Content-Type: application/json');

$host = 'localhost';
$db   = 'tabistats';
$user = 'giguerr231';
$pass = 'Miashs2025';
$charset = 'utf8mb4';

$dsn = "mysql:host=$host;dbname=$db;charset=$charset";
$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES   => false,
];

try {
    $pdo = new PDO($dsn, $user, $pass, $options);
} catch (\PDOException $e) {
    echo json_encode(["error" => "Erreur : " . $e->getMessage()]);
    exit;
}

$airport = isset($_GET['airport']) ? $_GET['airport'] : 'KIX';
$targetDate = isset($_GET['date']) ? $_GET['date'] : '2027-07-03';
$currency = isset($_GET['currency']) ? $_GET['currency'] : 'JPY';

// Devise
$sqlCurrency = "SELECT DATE(fetch_datetime) as date, exchange_rate FROM currency_rates WHERE currency_to = :currency ORDER BY fetch_datetime ASC";
$stmtCurrency = $pdo->prepare($sqlCurrency);
$stmtCurrency->execute(['currency' => $currency]);
$currencies = $stmtCurrency->fetchAll();

// Vols
$sqlFlights = "SELECT DATE(fetch_datetime) as date, price_eur, airline FROM flight_prices WHERE destination_airport = :airport AND departure_date = :targetDate ORDER BY fetch_datetime ASC";
$stmtFlights = $pdo->prepare($sqlFlights);
$stmtFlights->execute(['airport' => $airport, 'targetDate' => $targetDate]);
$flights = $stmtFlights->fetchAll();

echo json_encode(["currencies" => $currencies, "flights" => $flights]);
?>