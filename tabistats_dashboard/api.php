<?php
header('Content-Type: application/json');

// Configuration de la base de données
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
    echo json_encode(["error" => "Erreur de connexion : " . $e->getMessage()]);
    exit;
}

// Récupération des paramètres envoyés par l'interface
$airport = isset($_GET['airport']) ? $_GET['airport'] : 'KIX';
$targetDate = isset($_GET['date']) ? $_GET['date'] : '2027-07-05';
$currency = isset($_GET['currency']) ? $_GET['currency'] : 'JPY';

// 1. Récupération de l'historique de la Devise (avec filtre)
$sqlCurrency = "SELECT DATE(fetch_datetime) as date, exchange_rate 
                FROM currency_rates 
                WHERE currency_to = :currency 
                ORDER BY fetch_datetime ASC";

$stmtCurrency = $pdo->prepare($sqlCurrency);
$stmtCurrency->execute(['currency' => $currency]);
$currencies = $stmtCurrency->fetchAll();

// 2. Récupération de l'historique des Vols (avec filtres)
$sqlFlights = "SELECT DATE(fetch_datetime) as date, price_eur, airline 
               FROM flight_prices 
               WHERE destination_airport = :airport 
               AND departure_date = :targetDate 
               ORDER BY fetch_datetime ASC";

// Utilisation d'une requête préparée pour la sécurité
$stmtFlights = $pdo->prepare($sqlFlights);
$stmtFlights->execute([
    'airport' => $airport,
    'targetDate' => $targetDate
]);
$flights = $stmtFlights->fetchAll();

// On renvoie le tout en format JSON pour le JavaScript
echo json_encode([
    "currencies" => $currencies,
    "flights" => $flights
]);
?>