CREATE TYPE location_enum AS ENUM ('street', 'station', 'hub');
CREATE TYPE transport_enum AS ENUM ('train', 'bus', 'tram', 'taxi');
CREATE TYPE license_enum AS ENUM ('train license', 'taxi license', 'tram license', 'bus license');
CREATE TYPE infrastructure_enum AS ENUM ('road', 'rail', 'tramline');


CREATE TABLE IF NOT EXISTS location (
    location_id SERIAL PRIMARY KEY,
    location_name VARCHAR(50) NOT NULL,
    location_type location_enum NOT NULL,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL
);


CREATE TABLE IF NOT EXISTS roads_and_rails (
    road_rail_id SERIAL PRIMARY KEY,
    location_id INT REFERENCES location(location_id) NOT NULL,
    infrastructure_type infrastructure_enum NOT NULL
);


CREATE TABLE IF NOT EXISTS service_routes (
    route_id SERIAL PRIMARY KEY,
    route_name VARCHAR(50) NOT NULL,
    number_of_stops INT NOT NULL,
    journey_length_km DECIMAL(6,2) NOT NULL 
);


CREATE TABLE IF NOT EXISTS transport_routes (
    route_id INT REFERENCES service_routes(route_id) NOT NULL,
    location_id INT REFERENCES location(location_id) NOT NULL,
    stop_sequence INT NOT NULL,
    PRIMARY KEY (route_id, location_id) 
);


CREATE TABLE IF NOT EXISTS drivers (
    driver_id SERIAL PRIMARY KEY, 
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    license_type license_enum NOT NULL 
);


CREATE TABLE IF NOT EXISTS transport (
    transport_id SERIAL PRIMARY KEY,
    driver_id INT REFERENCES drivers(driver_id) NOT NULL,
    transport_type transport_enum NOT NULL,
    capacity INT NOT NULL CHECK (capacity <= 1200), 
    route_id INT REFERENCES service_routes(route_id) NOT NULL
);
