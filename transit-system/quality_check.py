from pipeline_logger import log

def run_row_count_checks(cursor):
    tables = ["location", "drivers", "service_routes", "roads_and_rails", "transport"]

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        count = cursor.fetchone()[0]
        if count == 0:
            log.error(f"Table '{table}' is empty.")
            return False
        else:
            log.info(f"Check passed for '{table}': {count} records have been verified.")
            return True
        
def run_business_logic_checks(cursor):
    checks_passed = True

    # Taxi capacity rules
    cursor.execute("SELECT COUNT(*) FROM transport WHERE transport_type = 'taxi' AND capacity > 4;")
    taxi_violations = cursor.fetchone()[0]
    if taxi_violations > 0:
        log.error(f"Found {taxi_violations} taxis that are over the realistic capacity")
        checks_passed = False
    else:
        log.info("All taxi capacities are within the realistic legal boundaries")

    # City bounds limit (maintaining a realistic city scale within coordinates)
    cursor.execute("SELECT COUNT(*) FROM location WHERE latitude NOT BETWEEN 40.6000 AND 40.8500;")
    coordinate_violations = cursor.fetchone()[0]
    if coordinate_violations > 0:
        log.error(f"Found {coordinate_violations} locations drifting outside the city grid")
        checks_passed = False
    else:
        log.info("Geographic coordinates checked and approved, align with city grid dimensions")

    return checks_passed

def execute_quality_suite(conn):
    # Data quality testing
    with conn.cursor() as cursor:
        counts_ok = run_row_count_checks(cursor)
        logic_ok = run_business_logic_checks(cursor)

    if counts_ok and logic_ok:
        log.info("All data quality assertions passed perfectly.")
    else:
        log.warning("Warning: Data quality checks finished with active errors. Check logs.")