use data_db;
CREATE TABLE weather (
    city_number INT NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY(city_number),
    city_name VARCHAR(255), 
    country VARCHAR(255), 
    latitude DECIMAL(10, 8) NOT NULL, 
    longitude DECIMAL(11, 8) NOT NULL, 
    temperature INT, 
    weather VARCHAR(255), 
    weather_desc VARCHAR(255)
     
);
