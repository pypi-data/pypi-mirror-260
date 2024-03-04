//recal.rs

use crate::EmbeddingManager;
use log::{info, warn};
use rand::prelude::*;
use std::collections::HashSet;

/// Performs a recall test on the given `EmbeddingManager`.
///
/// # Arguments
///
/// * `embedding_manager`: The `EmbeddingManager` to test.
/// * `test_percentage`: The percentage of embeddings to use for testing.
/// * `top_c`: The number of clusters to consider for cluster search.
/// * `top_n`: The number of nearest neighbors to return for both brute force and cluster search.
///
/// # Returns
///
/// The recall score as a float.
pub fn recal_test(
    embedding_manager: &EmbeddingManager,
    test_percentage: usize,
    top_c: usize,
    top_n: usize,
) -> f32 {
    // Calculate test size and log test parameters.
    let total_embeddings = embedding_manager.embeddings.len();
    let test_size = total_embeddings * test_percentage / 100;
    info!(
        "Starting recall test with {}% of embeddings, total test size: {}",
        test_percentage, test_size
    );

    // Shuffle embeddings and select test embeddings.
    let mut embeddings_vec: Vec<_> = embedding_manager.embeddings.iter().collect();
    let mut rng = thread_rng();
    embeddings_vec.shuffle(&mut rng);
    let test_embeddings: Vec<_> = embeddings_vec
        .into_iter()
        .take(test_size)
        .map(|(id, embedding)| (id.clone(), embedding.clone()))
        .collect();

    // Initialize counters for correct and total matches.
    let mut correct_matches = 0;
    let mut total_matches = 0;

    // Iterate over test embeddings and perform search comparisons.
    for (id, embedding) in test_embeddings.iter() {
        // Perform brute force search.
        let brute_force_results = match embedding_manager.brute_force_search(embedding.clone(), top_n, "id".to_string()) {
            Ok(results) => results,
            Err(e) => {
                warn!("Brute force search failed for embedding ID {}: {}", id, e);
                vec![]
            }
        };

        // Perform cluster search.
        let cluster_results = match embedding_manager.cluster_search(embedding.clone(), top_c, top_n, "id".to_string(), false) {
            Ok(results) => results,
            Err(e) => {
                warn!("Cluster search failed for embedding ID {}: {}", id, e);
                vec![]
            }
        };

        // Collect IDs from search results.
        let brute_force_ids: HashSet<_> = brute_force_results
            .iter()
            .map(|(id, _, _, _)| id.clone())
            .collect();
        let cluster_ids: HashSet<_> = cluster_results
            .iter()
            .map(|(id, _, _, _)| id.clone())
            .collect();

        // Log search IDs.
        info!("Brute force search IDs for {}: {:?}", id, brute_force_ids);
        info!("Cluster search IDs for {}: {:?}", id, cluster_ids);

        // Calculate intersection and update counters.
        let intersection = brute_force_ids.intersection(&cluster_ids).count();
        if intersection > 0 {
            info!(
                "Match found for {}: {} out of {} matches",
                id, intersection, top_n
            );
        } else {
            warn!("No matches found for {} between brute force and cluster search results.", id);
        }
        correct_matches += intersection;
        total_matches += top_n;
    }

    // Calculate and log recall score.
    let recall = correct_matches as f32 / total_matches as f32;
    info!("Recall test completed with score: {}", recall);

    recall
}