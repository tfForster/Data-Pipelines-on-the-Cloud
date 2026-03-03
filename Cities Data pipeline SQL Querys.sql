-- ========================================
-- Datenbank erstellen
-- ========================================
CREATE DATABASE IF NOT EXISTS cities_project;
USE cities_project;

-- ========================================
-- Tabelle: cities (Stammdaten)
-- ========================================
CREATE TABLE IF NOT EXISTS cities (
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    country_code CHAR(2),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    latitude_dms VARCHAR(50),
    longitude_dms VARCHAR(50),
    UNIQUE KEY unique_city_name (city_name)
);

-- ========================================
-- Tabelle: populations (jährliche Werte)
-- ========================================
CREATE TABLE IF NOT EXISTS populations (
    city_id INT NOT NULL,
    population BIGINT,
    timestamp_population DATE NOT NULL,
    PRIMARY KEY (city_id, timestamp_population),
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
        ON DELETE CASCADE
);

-- ========================================
-- Tabelle: weather (Forecast-Daten)
-- ========================================
CREATE TABLE IF NOT EXISTS weather (
    weather_id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT NOT NULL,
    forecast_time DATETIME NOT NULL,
    temperature FLOAT,
    humidity INT,
    wind_speed FLOAT,
    description VARCHAR(255),
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
        ON DELETE CASCADE
);

-- ========================================
-- Tabelle: flights
-- ========================================
CREATE TABLE flights (
    flight_id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT,
    flight_number VARCHAR(20),
    airline VARCHAR(100),
    arrival_airport VARCHAR(10),
    arrival_time DATETIME,
    status VARCHAR(50),
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

-- ========================================
-- TEST RESET (optional)
-- ========================================
-- SET FOREIGN_KEY_CHECKS = 0;
-- TRUNCATE TABLE weather;
-- TRUNCATE TABLE populations;
-- TRUNCATE TABLE cities;
-- TRUNCATE TABLE flights;
-- SET FOREIGN_KEY_CHECKS = 1;

-- ========================================
-- Quick Check
-- ========================================
SELECT * FROM cities;

SELECT * FROM populations;
SELECT * FROM weather;
SELECT * FROM flights;