from pipeline_logger import log

def generate_analytics_layer(conn):
    create_view_query = """
            CREATE OR REPLACE VIEW view_live_transit_status AS
            SELECT
                t.transport_id
                t.transport_type,
                t.capacity,
                d.first_name || ' ' || d.last_name AS driver_full_name,
                d.license_type AS driver_license,
                sr.route_name,
                sr.journey_length_km
            FROM transport t
            INNER JOIN drivers d ON t.driver_id = d.driver_id
            INNER JOIN service_routes sr ON t.route_id = sr.route_id;
    """

    with conn.cursor() as cursor:
        cursor.execute(create_view_query)
    conn.commit()

    log.info("Analytical reporting asset created successfully.")