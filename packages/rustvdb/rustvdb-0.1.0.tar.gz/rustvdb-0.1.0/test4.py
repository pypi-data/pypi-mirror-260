import time
from sklearn.datasets import make_blobs
import rustvdb

# Generate 50000 embeddings in 10 clusters
n_samples = 50000
n_clusters = 1000
X, y = make_blobs(n_samples=n_samples, centers=n_clusters, random_state=0)
print("created blobs")
print(X[0].tolist())

# Create an EmbeddingManager instance
manager = rustvdb.EmbeddingManager()

# Add embeddings to the manager
for i in range(n_samples):
    manager.add_embedding(str(i), "", X[i].tolist(), {})
print("added embeddings")

# Create clusters
start_time = time.time()
manager.create_clusters(n_clusters, 100)  # 100 iterations
clustering_time = time.time() - start_time
print(f"Clustering completed in {clustering_time:.2f} seconds.")

# Choose a random query embedding
query_index = 10
query_embedding = X[query_index]

# Brute-force search
start_time = time.time()
brute_force_results = manager.brute_force_search(query_embedding.tolist(), 5, "full")
brute_force_time = time.time() - start_time
print(f"Brute-force search completed in {brute_force_time*1000:.2f} ms.")

# Cluster-based search
start_time = time.time()
cluster_results = manager.cluster_search(query_embedding.tolist(), 2, 5, "full", False)
cluster_time = time.time() - start_time
print(f"Cluster-based search completed in {cluster_time*1000:.2f} ms.")

# Print some results (you can customize this)
print("\nBrute-force search results:")
for result in brute_force_results:
    print(f"ID: {result[0]}, Similarity: {result[3]:.4f}")

print("\nCluster-based search results:")
for result in cluster_results:
    print(f"ID: {result[0]}, Similarity: {result[3]:.4f}")