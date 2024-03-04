
from rustvdb import EmbeddingManager
import numpy as np
import random
import string
import time
import pickle
import os


os.environ["RUST_LOG"] = "info"

def python_brute_force_search(query_embedding, embeddings, top_n):
    """Perform a brute force search to find the most similar embeddings.
    
    Args:
        query_embedding (list): The query embedding as a list of floats.
        embeddings (dict): A dictionary of embeddings with IDs as keys and (vector, content) tuples as values.
        top_n (int): The number of top similar embeddings to return.
    
    Returns:
        list: A list of tuples containing the ID, content, and similarity score of the top N similar embeddings.
    """
    similarities = []
    for (id, content, vector, metadata) in embeddings:
        similarity = cosine_similarity(query_embedding, vector)
        similarities.append((id, content, vector, metadata, similarity))
    
    # Sort by similarity in descending order and return the top N results
    sorted_similarities = sorted(similarities, key=lambda x: x[2], reverse=True)[:top_n]
    return sorted_similarities

def cosine_similarity(vec1, vec2):
    """Calculate the cosine similarity between two vectors."""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    else:
        return dot_product / (norm_vec1 * norm_vec2)

def generate_fake_embedding(dimension=768):
    content = ''.join(random.choices(string.ascii_letters + ' ', k=50))
    embedding = np.random.rand(dimension).tolist()
    metadata = {"source": "generated"}
    return content, embedding, metadata

def test_update_embedding(manager, id, new_embedding, new_metadata):
    print(f"Updating embedding for ID: {id}")
    manager.update_embedding(id, new_embedding, new_metadata)
    print(f"Updated embedding and metadata for {id}.")

def test_delete_embedding(manager, id):
    print(f"Deleting embedding for ID: {id}")
    manager.delete_embedding(id)
    result = manager.get_embedding_by_id(id)
    assert result is None, f"Embedding {id} was not properly deleted."
    print(f"Successfully deleted embedding for {id}.")

def test_get_embedding_by_id(manager, id):
    print(f"Retrieving embedding for ID: {id}")
    result = manager.get_embedding_by_id(id)
    if result:
        content, embedding, metadata = result
        print(f"Retrieved embedding for {id}: Embedding: {embedding}, Content: {content}, Metadata: {metadata}")
    else:
        print(f"No embedding found for ID: {id}")

def measure_performance(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    print(f"Execution time for {func.__name__}: {end_time - start_time:.4f} seconds")
    return result

def load_embeddings_from_file(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def save_embeddings_to_file(embeddings, filename):
    with open(filename, 'wb') as f:
        pickle.dump(embeddings, f)

def main():
    manager = EmbeddingManager()
    # Prepare the arguments required by vertex_embedding
    id = "your_id"
    title = "Sample Title"
    content = "Sample content here."
    metadata = {"test":"test"}  # Assuming metadata is a dictionary
    project_id = "alan-genai-search"
    location = "us-central1"

    # Call vertex_embedding
    # Note: If vertex_embedding is async, you'll need to run it within an async context
    embeddings = manager.vertex_embedding(id, title, content, metadata, project_id, location, "retrieve")
    if embeddings is not None:
        print("Retrieved embeddings:", type(embeddings))
    else:
        print("No embeddings were retrieved.")
    # Example usage
    exit()
    id_to_retrieve = "your_id"  # Assuming this ID exists
    test_get_embedding_by_id(manager, id_to_retrieve)
    manager.add_embedding("id1", "This is a sample embedding.", [0.1, 0.2, 0.3], {"author": "John Doe"})
    manager.brute_force_search( [0.1,0.2,0.3], 1, "full")
    exit()   
    filename = "./embeddings.pkl"
    manager = EmbeddingManager()
    if os.path.exists(filename):
        print(f"Loading embeddings from {filename}")
        raw_embeddings = load_embeddings_from_file(filename)
        manager.add_embeddings_bulk(raw_embeddings)
        print(f"Loaded {len(raw_embeddings)} embeddings into the manager.")
    else:
        print("Generating new embeddings...")
        raw_embeddings = []
        num_embeddings = 10000#00  # Adjust as needed
        dimension = 768  # Example dimension size for the embeddings

        for i in range(num_embeddings):
            content, embedding, metadata = generate_fake_embedding(dimension)
            id = f"emb_{i}"
            raw_embeddings.append((id, content, embedding, metadata))

        # Bulk add to the manager
        manager.add_embeddings_bulk(raw_embeddings)
        print(f"Added {num_embeddings} embeddings to the manager.")

        # Save the newly generated embeddings to a file
        save_embeddings_to_file(raw_embeddings, filename)
        print(f"Embeddings saved to {filename}")

    # Random query embedding
    dimension = 768 
    top_c = 4 #amount of clusters to search
    top_n = 2 #amount of results to return
    n_clusters = 10
    n_iterations = 100

    manager.create_clusters(n_clusters, n_iterations)

    query_embedding = np.random.rand(dimension).tolist()
    while True:
        print("Python Brute Force Search:")
        results_python = measure_performance(python_brute_force_search, query_embedding, raw_embeddings, top_n)
        for id, content, vector, metadata, similarity in results_python:
            content = None
            print(f"ID: {id}, Content: {content}, Similarity: {similarity}")
        # Brute Force Search
        print("Brute Force Search:")
        results_brute = measure_performance(manager.brute_force_search, query_embedding, top_n, "full")
        for id, vector, content, similarity in results_brute:
            print(f"ID: {id}, Vector: {vector}, Content: {content}, Similarity: {similarity}")

        # Cluster Search
        print("\nCluster Search:")
        # Assuming 'manager' has a method 'cluster_search' taking query_embedding, n_clusters, and top_n as parameters
        results_cluster = measure_performance(lambda q, c, t: manager.cluster_search(q, c, t, "content", False), query_embedding, top_c, top_n)
        for id, vector, content, similarity in results_cluster:
            print(f"ID: {id}, Similarity: {similarity}")
        time.sleep(2)
        break

    # Call the recal_test method from Rust
    recall_score = manager.recal_test(10, top_c, top_n)
    print(f"Recall score: {recall_score}")

    # Example usage
    id_to_update = "emb_0"  # Assuming this ID exists
    new_embedding = np.random.rand(768).tolist()  # New embedding vector
    new_metadata = {"source": "updated", "note": "This is an updated embedding."}
    test_update_embedding(manager, id_to_update, new_embedding, new_metadata)

    # Example usage
    id_to_delete = "emb_1"  # Assuming this ID exists
    test_delete_embedding(manager, id_to_delete)

    # Example usage
    id_to_retrieve = "emb_0"  # Assuming this ID exists
    test_get_embedding_by_id(manager, id_to_retrieve)
    print('1')
    manager.save_to_file()
    print('2')


main()




