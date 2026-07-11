# city-transit-system
# Fictional Smart City Transit Platform


In this project, I wanted to move away from standard API tutorials and challenge myself with **database design, data modeling, and infrastructure automation**. I decided to model the data backbone for a fictional smart city transit network, handling everything from designing the relational schema to automating the pipeline.

The goal wasn't just to load data, but to learn how real-world data systems move data from raw, operational storage (**OLTP**) into structured assets for data analysts (**OLAP**).

---

## What I Designed (Schema & Data Structure)

Instead of using a single flat file, I wanted to practice relational database mapping. I built a schema spread across **6 interconnected JSON datasets** with custom drop-down rules (ENUMs) to keep the data clean.

### The Tables:
*   **`location`**: The geographic base of the city. To keep the data realistic, I locked all coordinates to a tight 15-mile grid (simulating a dense Brooklyn-style neighborhood) so the points wouldn't scatter across the globe.
*   **`roads_and_rails`**: Maps what kind of transit infrastructure exists at each location.
*   **`drivers`**: The master workforce roster.
*   **`service_routes`**: General route tracking profiles.
*   **`transport`**: Active transit vehicles (buses, trains, trams, taxis). 
*   **`transport_routes`**: A **Bridge Table** I added to cleanly resolve a complex many-to-many relationship between transit routes and physical station locations without duplicating data.

---

## The Tech Stack I Learned

*   **Language:** Python 3.12.4
*   **Database Engine:** PostgreSQL 15
*   **Infrastructure:** Docker & Docker Compose (Implementation due soon)
*   **Database Driver:** Psycopg2

---

## Key Problems I Had to Solve

### 1. Stopping Taxis from Holding 1,200 People (Data Quality)
When generating mock data, generic tools don't understand real-world business logic. I was running into bugs where taxis randomly held 1,200 people, and trains held 4. To fix this, I learned how to write custom **Inline Conditional Logic** in Mockaroo to tie capacities to specific vehicle types:
```javascript
if transport_type == 'taxi' then random(1, 4)
elsif transport_type == 'bus' then random(30, 80)
else random(200, 1200) end
```

### 2. Preventing Database Crashes (Idempotency)
I learned that databases are incredibly strict about foreign key relationships. If my script tried to load a vehicle before loading its driver, the whole pipeline would crash. 
*   **The Fix:** I carefully ordered the script to load master tables first.
*   **The Extra Step:** I implemented `ON CONFLICT DO NOTHING` clauses. This makes my script **idempotent**, meaning you can run it 100 times and it will safely skip over rows it already processed instead of crashing on duplicates.

### 3. Automating Setup via Docker
I wanted this project to be completely reproducible for anyone reviewing my code. Even though I started building this locally, I wrapped the database in a `docker-compose.yml` file. If someone else clones this project, Docker will automatically download Postgres, open port `5432`, and run my `schema.sql` file to build the tables on boot.

---

## The 3 Pipeline Layers I Built

To make my ingestion engine (`build.py`) mimic an enterprise system, I expanded it into three distinct software layers:

*   **Layer 1: Professional Logging (`pipeline_logger.py`)**: I moved away from plain `print()` statements and built a dual-handler logger. It writes a permanent timestamped record to a `pipeline.log` file for debugging while still printing clean progress bars to the screen.
*   **Layer 2: The Automated Gatekeeper Suite (`data_quality_checks.py`)**: I wrote a testing layer that queries the database right after ingestion. It checks row counts to ensure no data was dropped and scans rows to flag any out-of-bounds rule violations.
*   **Layer 3: Analytical SQL Transformation (`create_analytical_views.py`)**: Relational tables are great for apps, but messy for data analysts. I wrote a final step that executes a multi-table `INNER JOIN` in SQL, flattening my data into a single clean view (`view_live_transit_status`) that is instantly ready for a dashboard tool like PowerBI.

---


---



