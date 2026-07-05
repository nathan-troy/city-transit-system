import json
import os
import psycopg2

# Importing pipeline layers
from pipeline_logger import log
from quality_check import execute_quality_suite
from analytical_views import generate_analytics_layer

# Connection Config
DB_CONFIG = {
    "dbname": "smart_transit_db",
    "user": "postgres",
    "password": "pass123",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def load_json_table(conn, file_path, query_template, parse_record_func):
    with conn.cursor() as cursor:
        with open(file_path, mode='r', encoding='utf-8') as file:
            records = json.load(file)
            for record in records:
                # Transforming JSON objects into a clean tuple of values
                data_tuple = parse_record_func(record)
                cursor.execute(query_template, data_tuple)
        conn.commit()


# Data Mapping Functions
def parse_service_route(record):
    # Map JSON keys to db columns
    return (
        int(record['route_id']),
        record['route_name'],
        int(record['number_of_stops']),
        float(record['journey_length_km'])
    )
def parse_drivers(record):
    return (
        int(record['driver_id']),
        record['first_name'],
        record['last_name'],
        record['license_type']
    )
def parse_location(record):
    return (
        int(record['location_id']),
        record['location_name'],
        record['location_type'],
        float(record['latitude']),
        float(record['longitude'])
    )
def parse_roads_and_rails(record):
    return (
        int(record['road_rail_id']),
        int(record['location_id']),
        record['infrastructure_type']
    )
def parse_transport_routes(record):
    return (
        int(record['route_id']),
        int(record['location_id']),
        int(record['stop_sequence'])
    )
def parse_transport(record):
    return (
        int(record['transport_id']),
        int(record['driver_id']),
        record['transport_type'],
        int(record['capacity']),
        int(record['route_id'])
    )


# Main
def run_pipeline():

    try:
        with get_db_connection() as conn:
            
            insert_location = """
                INSERT INTO location (location_id, location_name, location_type, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (location_id) DO NOTHING;
            """
            load_json_table(conn, "raw_data/location.json", insert_location, parse_location)

            insert_drivers = """
                INSERT INTO drivers (driver_id, first_name, last_name, license_type)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (driver_id) DO NOTHING;
            """
            load_json_table(conn, "raw_data/drivers.json", insert_drivers, parse_drivers)

            insert_routes = """
                INSERT INTO service_routes (route_id, route_name, number_of_stops, journey_length_km)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (route_id) DO NOTHING;
            """
            load_json_table(conn, "raw_data/service_routes.json", insert_routes, parse_service_route) 

            insert_roads_rails = """
                INSERT INTO roads_and_rails (road_rail_id, location_id, infrastructure_type)
                VALUES (%s, %s, %s)
                ON CONFLICT (road_rail_id) DO NOTHING;
            """
            load_json_table(conn, "raw_data/roads_and_rails.json", insert_roads_rails, parse_roads_and_rails)

            insert_transport_routes = """
                INSERT INTO transport_routes (route_id, location_id, stop_sequence)
                VALUES (%s, %s, %s)
                ON CONFLICT (route_id, location_id) DO NOTHING;
            """
            load_json_table(conn, "raw_data/transport_routes.json", insert_transport_routes, parse_transport_routes)

            insert_transport = """
                INSERT INTO transport (transport_id, driver_id, transport_type, capacity, route_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (transport_id) DO NOTHING;
            """
            load_json_table(conn, "raw_data/transport.json", insert_transport, parse_transport)

            # Data Quality Validation
            execute_quality_suite(conn)

            # Transformation Layer
            generate_analytics_layer(conn)

    except Exception as e:
        log.error(f"Pipeline failed with error: {e}")
    
if __name__ == "__main__":
    run_pipeline()
