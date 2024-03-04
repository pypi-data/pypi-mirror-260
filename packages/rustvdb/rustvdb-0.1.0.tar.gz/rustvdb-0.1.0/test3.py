from rustvdb import EmbeddingManager  # Import the init function


manager = EmbeddingManager()

import os


os.environ["RUST_LOG"] = "debug"

queries = [
    {
        "id": "query1",
        "title": "Average Engine Temperature by Truck ID",
        "content": "This query calculates the average engine temperature for each truck, providing insights into which trucks may be running hotter than usual.",
        "metadata": {"sql": """SELECT truck_id, AVG(engine_temp) AS average_engine_temperature FROM `truckllm.truck_data` GROUP BY truck_id;"""}
    },
    {
        "id": "query2",
        "title": "Count of Trucks with Maintenance Flags",
        "content": "This query counts how many trucks have a maintenance flag set, indicating potential issues that need addressing.",
        "metadata": {"sql": """SELECT COUNT(*) AS trucks_needing_maintenance FROM `truckllm.truck_data` WHERE maintenance_flag = TRUE;"""}
    },
    {
        "id": "query3",
        "title": "Maximum Fuel Level and Location",
        "content": "This query finds the maximum fuel level recorded and the corresponding location, which could help in identifying fuel efficiency or refueling patterns.",
        "metadata": {"sql": """SELECT MAX(fuel_level) AS max_fuel_level, location_lat, location_lng FROM `truckllm.truck_data` GROUP BY location_lat, location_lng ORDER BY max_fuel_level DESC LIMIT 1;"""}
    },
    {
        "id": "query4",
        "title": "Daily Mileage for Each Truck",
        "content": "Calculates the total mileage covered by each truck on a daily basis, useful for monitoring daily operations and identifying outliers.",
        "metadata": {"sql": """SELECT truck_id, DATE(timestamp) AS date, SUM(mileage) AS total_daily_mileage FROM `truckllm.truck_data` GROUP BY truck_id, date;"""}
    },
    {
        "id": "query5",
        "title": "Top 5 Most Frequent Error Codes",
        "content": "Identifies the top 5 most frequently reported error codes, aiding in pinpointing common mechanical or operational issues.",
        "metadata": {"sql": """SELECT error_codes, COUNT(*) AS frequency FROM `truckllm.truck_data` WHERE error_codes IS NOT NULL GROUP BY error_codes ORDER BY frequency DESC LIMIT 5;"""}
    },
    {
        "id": "query6",
        "title": "Rolling Average Engine Temperature",
        "content": "Calculates a 7-day rolling average of engine temperature for each truck, useful for spotting trends or changes in engine performance over time.",
        "metadata": {"sql": """SELECT truck_id, DATE(timestamp) AS date, AVG(engine_temp) OVER (PARTITION BY truck_id ORDER BY DATE(timestamp) RANGE BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_avg_temp FROM `truckllm.truck_data`;"""}
    },
    {
        "id": "query7",
        "title": "Cumulative Mileage per Truck",
        "content": "Tracks the cumulative mileage for each truck over time, providing insight into usage and potential maintenance schedules.",
        "metadata": {"sql": """WITH DailyMileage AS (SELECT truck_id, DATE(timestamp) AS date, SUM(mileage) AS daily_mileage FROM `truckllm.truck_data` GROUP BY truck_id, DATE(timestamp)) SELECT truck_id, date, SUM(daily_mileage) OVER (PARTITION BY truck_id ORDER BY date) AS cumulative_mileage FROM DailyMileage ORDER BY truck_id, date;;"""}
    },
    {
        "id": "query8",
        "title": "Detecting Outliers in Engine Temperature",
        "content": "Identifies outlier readings in engine temperature using the standard deviation method (mean ± 2*stddev) for each truck.",
        "metadata": {"sql": """WITH stats AS ( SELECT truck_id, AVG(engine_temp) AS avg_temp, STDDEV(engine_temp) AS stddev_temp FROM `truckllm.truck_data` GROUP BY truck_id) SELECT t.*, s.avg_temp, s.stddev_temp FROM `truckllm.truck_data` t JOIN stats s ON t.truck_id = s.truck_id WHERE engine_temp < (s.avg_temp - 2 * s.stddev_temp) OR engine_temp > (s.avg_temp + 2 * s.stddev_temp);"""}
    },
    {
        "id": "query9",
        "title": "Monthly Fuel Efficiency by Truck",
        "content": "Calculates fuel efficiency (mileage per unit of fuel) for each truck on a monthly basis, highlighting potential variations in vehicle performance or usage.",
        "metadata": {"sql": """SELECT truck_id, EXTRACT(YEAR FROM timestamp) AS year, EXTRACT(MONTH FROM timestamp) AS month, SUM(mileage) / SUM(fuel_level) AS fuel_efficiency FROM `truckllm.truck_data` GROUP BY truck_id, year, month;"""}
    },
    {
        "id": "query10",
        "title": "Sequential Anomalies in Oil Pressure",
        "content": "Uses the LAG function to compare current oil pressure readings against the previous reading for each truck, identifying significant drops that could indicate mechanical issues.",
        "metadata": {"sql": """SELECT truck_id, timestamp, oil_pressure, LAG(oil_pressure) OVER (PARTITION BY truck_id ORDER BY timestamp) AS previous_oil_pressure, CASE WHEN oil_pressure < LAG(oil_pressure) OVER (PARTITION BY truck_id ORDER BY timestamp) - 10 THEN 'Significant drop' ELSE 'Normal' END AS oil_pressure_change FROM `truckllm.truck_data`;"""}
    }
]

import random

def generate_fake_data(num_entries, colors):
    fake_data = []
    for _ in range(num_entries):
        fake_entry = {
            "id": f"fake_id_{random.randint(1, 1000000000)}",  # Generate random IDs
            "title": "",  # You can customize this if needed
            "content": random.choice(colors),
            "metadata": {}  # You can add fake metadata if required
        }
        fake_data.append(fake_entry)
    return fake_data

colors = [
    "red", "green", "blue", "yellow", "orange", "purple", "pink", "gray", "brown", "cyan", "magenta", "lime", 
]

num_entries = 100  # Example: Generate 100 fake entries

queries = generate_fake_data(num_entries, colors)

# Set up the environment for vertex_embedding
project_id = "alan-genai-search"
location = "us-central1"
qps = 100  # For example

# Initialize vertex embedding environment
manager.init_vertex_embedding(project_id, location, qps)

# Now you can use vertex_embedding as before
for each in queries:
    id = each["id"]
    title = each["title"]
    content = each["content"]
    metadata = each["metadata"]  # Assuming metadata is a dictionary

    # Call vertex_embedding
    embeddings = manager.vertex_embedding(id, title, content, metadata, "load")

query_embedding_text = "blue"
query_embedding = manager.vertex_embedding("", "", query_embedding_text, {}, "retrieve")
print(len(query_embedding))

import json
example_queries = "blue"
top_n = 1
sql_match = manager.brute_force_search(query_embedding, top_n, "content")
for id, embedding, content, similarity in sql_match:
    content = json.loads(content)
    print(f"content: {content}, sim: {similarity}")
    #print(f"Id: {id},\nTitle: {title},\nContent: {content['content']},\nmetadata: {content['metadata']['sql']},\nSimilarity: {similarity}\n")
    #example_queries = content['metadata']['sql']


# Random query embedding
dimension = 768 
top_c = 5 #amount of clusters to search
top_n = 2 #amount of results to return
n_clusters = -1
n_iterations = 100

a = manager.create_clusters(n_clusters, n_iterations)
print(a)

a=manager.cluster_search(query_embedding, top_c, top_n, "content", True)
print(a)