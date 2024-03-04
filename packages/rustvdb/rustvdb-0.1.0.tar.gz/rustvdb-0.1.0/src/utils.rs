// utils.rs

// Import the necessary modules and types at the beginning.
use ndarray::Array2;
use std::collections::HashMap;

/// Calculates the cosine similarity between two vectors.
/// 
/// The function computes the cosine similarity as the dot product
/// of the vectors divided by the product of their magnitudes.
/// If either vector has a magnitude of 0, the similarity is 0.
///
/// # Arguments
///
/// * `vec1` - A slice of f32 representing the first vector.
/// * `vec2` - A slice of f32 representing the second vector.
///
/// # Returns
///
/// The cosine similarity as a floating point value.
#[inline]
pub fn cosine_similarity(vec1: &[f32], vec2: &[f32]) -> f32 {
    let dot_product: f32 = vec1.iter().zip(vec2.iter()).map(|(a, b)| a * b).sum();
    let magnitude1: f32 = vec1.iter().map(|v| v.powi(2)).sum::<f32>().sqrt();
    let magnitude2: f32 = vec2.iter().map(|v| v.powi(2)).sum::<f32>().sqrt();

    if magnitude1 == 0.0 || magnitude2 == 0.0 {
        0.0
    } else {
        dot_product / (magnitude1 * magnitude2)
    }
}

/// Converts a HashMap of embedding vectors to an ndarray::Array2<f32> for clustering.
///
/// This function takes a reference to a HashMap where each key is a String
/// representing the embedding ID, and each value is a Vec<f32> representing
/// the embedding vector. It converts this map into a 2D ndarray
/// where each row corresponds to an embedding vector.
///
/// # Arguments
///
/// * `embeddings` - A reference to a HashMap containing the embedding vectors.
///
/// # Returns
///
/// An Array2<f32> containing the embeddings in a 2D format suitable for clustering.
///
/// # Panics
///
/// Panics if the embeddings HashMap is empty, indicating there are no embeddings to convert.
pub fn hashmap_to_ndarray(embeddings: &HashMap<String, Vec<f32>>) -> Array2<f32> {
    if embeddings.is_empty() {
        panic!("No embeddings found");
    }

    let n_embeddings = embeddings.len();
    let dimension = embeddings.values().next().unwrap().len(); // Safe due to the above check

    let mut array = Array2::<f32>::zeros((n_embeddings, dimension));

    for (i, emb) in embeddings.values().enumerate() {
        for (j, &value) in emb.iter().enumerate() {
            array[[i, j]] = value;
        }
    }

    array
}

