CREATE TABLE currency_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fetch_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    currency_from CHAR(3) NOT NULL, -- ex: 'EUR'
    currency_to CHAR(3) NOT NULL,   -- ex: 'JPY'
    exchange_rate DECIMAL(10, 4) NOT NULL, -- 4 decimales pour la precision financiere
    
    -- On s'assure qu'on ne stocke qu'un seul taux par jour et par paire de devises
    CONSTRAINT unique_daily_rate UNIQUE (currency_from, currency_to, fetch_datetime) 
);

CREATE TABLE flight_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fetch_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Critères de recherche
    departure_date DATE NOT NULL,
    return_date DATE NOT NULL,
    origin_airport CHAR(3) NOT NULL,      -- Code IATA, ex: 'CDG' pour Paris
    destination_airport CHAR(3) NOT NULL, -- Code IATA, ex: 'HND' ou 'NRT' pour Tokyo
    
    -- Donnees du vol trouve
    airline VARCHAR(100) NOT NULL,
    price_eur DECIMAL(8, 2) NOT NULL,
    
    -- Mesures de confort (essentielles pour l'analyse)
    duration_outbound_mins INT NOT NULL,  -- Stocke en minutes pour faciliter le tri/calcul
    duration_return_mins INT NOT NULL,
    stops_outbound INT NOT NULL DEFAULT 0,
    stops_return INT NOT NULL DEFAULT 0
);

CREATE VIEW v_daily_flight_trends AS
SELECT 
    DATE(fetch_datetime) as extraction_day,
    departure_date,
    destination_airport,
    MIN(price_eur) as cheapest_flight,
    ROUND(AVG(price_eur), 2) as average_price,
    MAX(price_eur) as most_expensive_flight
FROM 
    flight_prices
GROUP BY 
    DATE(fetch_datetime), departure_date, destination_airport;
    