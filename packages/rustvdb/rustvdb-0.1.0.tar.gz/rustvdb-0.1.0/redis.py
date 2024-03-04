import numpy as np
import redis

# Configuration for Redis connection
redis_host = '10.225.192.163'
redis_port = 6379

# Connect to Redis
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

# Define the FT.CREATE command
index_name = 'idx'
hash_field_key = 'hash_key'
command = f'FT.CREATE {index_name} ON HASH PREFIX 1 {hash_field_key}: SCHEMA {hash_field_key} VECTOR HNSW 10 TYPE FLOAT32 DIM 20 DISTANCE_METRIC COSINE M 4 EF_CONSTRUCTION 100'

# Execute the command
try:
    response = r.execute_command(command)
    print(f'Response: {response}')
except Exception as e:
    print(f'Error: {e}')