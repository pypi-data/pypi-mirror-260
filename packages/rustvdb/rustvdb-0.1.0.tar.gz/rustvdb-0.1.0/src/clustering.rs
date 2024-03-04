//clustering.rs

use ndarray::{Array1, Array2};
use kmeans::{KMeans, KMeansConfig};
use log::{info, debug, error};
use rayon::prelude::*;
use std::sync::Arc;
use std::time::Instant;
use std::cmp::Ordering;
use std::collections::HashMap;
use std::panic::{self, AssertUnwindSafe};
use serde::Serialize;



#[cfg(target_arch = "x86_64")]
use std::arch::x86_64::*;

#[cfg(target_arch = "x86_64")]
#[target_feature(enable = "avx2")]
pub unsafe fn simd_distance(v1: &Array1<f32>, v2: &Array1<f32>) -> f32 {
    assert_eq!(v1.len(), v2.len(), "Vectors must be the same length");

    const VEC_LEN: usize = 8; // AVX2 vector length

    let (v1_ptr, v2_ptr) = (v1.as_ptr(), v2.as_ptr());
    let mut distance_sum: __m256 = _mm256_setzero_ps();

    let mut i = 0;
    while i + VEC_LEN <= v1.len() {
        let v1_vec = _mm256_loadu_ps(v1_ptr.add(i));
        let v2_vec = _mm256_loadu_ps(v2_ptr.add(i));

        let diff = _mm256_sub_ps(v1_vec, v2_vec);
        let squared_diff = _mm256_mul_ps(diff, diff);

        distance_sum = _mm256_add_ps(distance_sum, squared_diff);

        i += VEC_LEN;
    }

    // Reduce the vector sum to a single sum
    let mut sum = _mm256_hadd_ps(distance_sum, distance_sum); // Horizontal add pairs of elements
    sum = _mm256_hadd_ps(sum, sum); // Repeat to cover all elements
    let lower_half = _mm256_extractf128_ps(sum, 0); // Lower half of the result
    let upper_half = _mm256_extractf128_ps(sum, 1); // Upper half of the result
    let final_sum = _mm_add_ss(lower_half, upper_half); // Add the lower and upper half

    // Handle remaining elements
    let mut remaining_sum = 0.0;
    while i < v1.len() {
        let diff = v1[i] - v2[i];
        remaining_sum += diff * diff;
        i += 1;
    }

    let final_scalar_sum = _mm_cvtss_f32(final_sum) + remaining_sum; // Convert final sum to scalar and add remaining sum

    final_scalar_sum.sqrt()
}


/// Generates a detailed hashmap for each cluster containing its item count and ID.
///
/// This function iterates through a slice of `Cluster` instances and creates a nested hashmap.
/// The outer hashmap's key is the cluster index, and its value is another hashmap with
/// strings representing the cluster's details such as item count and cluster ID.
///
/// # Arguments
/// * `clusters` - A slice of `Cluster` representing the clusters to generate info for.
///
/// # Returns
/// A `HashMap` where the key is the cluster index and the value is another `HashMap` with
/// the cluster's details.
fn generate_cluster_info_hashmap(clusters: &[Cluster]) -> HashMap<usize, HashMap<&'static str, String>> {
    let mut hashmap = HashMap::new();
    for (i, cluster) in clusters.iter().enumerate() {
        let mut details = HashMap::new();
        details.insert("items_count", cluster.embeddings.len().to_string());
        details.insert("cluster_id", i.to_string());
        hashmap.insert(i, details);
    }
    hashmap
}

/// Calculates the cosine similarity between two vectors.
///
/// The cosine similarity is a measure that calculates the cosine of the angle between
/// two vectors projected in a multi-dimensional space.
///
/// # Arguments
/// * `v1` - A reference to the first vector.
/// * `v2` - A reference to the second vector.
///
/// # Returns
/// The cosine similarity between the two vectors as a floating-point number.
fn cosine_similarity(v1: &Array1<f32>, v2: &Array1<f32>) -> f32 {
    let dot_product = v1.dot(v2);
    let norm_v1 = v1.dot(v1).sqrt();
    let norm_v2 = v2.dot(v2).sqrt();
    dot_product / (norm_v1 * norm_v2)
}

/// Calculates the Euclidean distance between two vectors.
///
/// The Euclidean distance represents the shortest distance between two points
/// in the multi-dimensional space.
///
/// # Arguments
/// * `v1` - A reference to the first vector.
/// * `v2` - A reference to the second vector.
///
/// # Returns
/// The Euclidean distance between the two vectors as a floating-point number.
fn euclidean_distance(v1: &Array1<f32>, v2: &Array1<f32>) -> f32 {
    (v1 - v2).mapv(|x| x.powi(2)).sum().sqrt()
}

/// Represents a single cluster, including its centroid and associated embeddings.
#[derive(Clone, Debug)]
pub struct Cluster {
    centroid: Array1<f32>,
    embeddings: Vec<usize>,
}

/// Manages the overall clustering process, including storing clusters, embeddings, and cluster information.
pub struct ClusteringManager {
    pub clusters: Vec<Cluster>,
    pub embeddings: Array2<f32>,
    pub cluster_infos: Vec<ClusterInfo>,
}

/// Contains detailed information about clusters, including a map of cluster details,
/// silhouette score for evaluating clustering quality, and the number of clusters.
#[derive(Debug, Serialize, Clone)]
pub struct ClusterInfo {
    pub cluster_points: HashMap<usize, HashMap<&'static str, String>>,
    pub silhouette_score: f32,
    pub n_clusters: usize,
}



/// Manages clustering operations and data.
///
/// `ClusteringManager` is responsible for managing the lifecycle of clustering operations,
/// including the initialization of clusters, calculation of silhouette scores for assessing
/// clustering quality, and providing access to cluster information and results.
/// It encapsulates the dataset's embeddings, the clusters formed from these embeddings,
/// and detailed information about each cluster.
///
/// # Examples
///
/// Basic usage:
///
/// ```rust
/// let embeddings: Array2<f32> = Array2::from_shape_vec((10, 2), vec![
///     /* dataset embeddings here */
/// ]).unwrap();
/// let n_clusters = 3;
/// let n_iterations = 100;
///
/// let clustering_manager = ClusteringManager::new(embeddings, n_clusters as isize, n_iterations);
///
/// // Access cluster information
/// let cluster_info = clustering_manager.get_cluster_info();
/// println!("{:?}", cluster_info);
///
/// // Find nearest centroids to a new embedding
/// let query_embedding = Array1::from_vec(vec![/* query embedding here */]);
/// let nearest_centroids = clustering_manager.find_nearest_centroids(&query_embedding, 2);
/// println!("Nearest centroids: {:?}", nearest_centroids);
///
/// // Aggregate results from nearest clusters
/// let aggregated_results = clustering_manager.aggregate_results_from_clusters(nearest_centroids, &query_embedding, 5);
/// println!("Aggregated results: {:?}", aggregated_results);
/// ```
///
/// This struct is a key component of the clustering system, providing methods to perform
/// clustering, retrieve information about the clusters, and analyze individual data points
/// in the context of the generated clusters.
impl ClusteringManager {    /// Constructs a new `ClusteringManager` instance.
    ///
    /// This method initializes the clustering process with the given embeddings, number of clusters,
    /// and iterations. It determines the best number of clusters (if not specified) and performs
    /// clustering to populate the `ClusteringManager` with clusters, their information, and a
    /// silhouette score indicating the quality of the clustering.
    ///
    /// # Arguments
    /// * `embeddings` - A 2D array of embeddings (features) for clustering.
    /// * `n_clusters` - The desired number of clusters. If `-1`, the method will attempt to
    ///   determine the optimal number of clusters within a preset range.
    /// * `n_iterations` - The number of iterations to run the clustering algorithm.
    ///
    /// # Returns
    /// A new instance of `ClusteringManager` populated with the results of the clustering process.
    ///
    /// # Panics
    /// This function will panic if `n_clusters` is specified but cannot be converted to a `usize`.
    pub fn new(embeddings: Array2<f32>, n_clusters: isize, n_iterations: usize) -> Self {
        let n_samples = embeddings.nrows();
        let dimension = embeddings.ncols();

        // Convert embeddings to f64 for compatibility with kmeans crate
        let samples: Vec<f64> = embeddings.iter().map(|&x| x as f64).collect();

        // Determine the best number of clusters (and corresponding cluster info, silhouette score, and clusters)
        // through the build_clusters method, which internally uses perform_clustering
        let (cluster_infos, clusters) =
            if n_clusters == -1 {
                Self::build_clusters(&samples, n_samples, dimension, n_iterations, Some((2, 16)))
            } else {
                let n_clusters_usize = n_clusters.try_into().unwrap_or_else(|_| {
                    error!("Failed to convert n_clusters to usize");
                    panic!("Failed to convert n_clusters to usize");
                });
                Self::build_clusters(&samples, n_samples, dimension, n_iterations, Some((n_clusters_usize, n_clusters_usize)))
            };

        // Instantiate ClusteringManager with the directly obtained clusters and cluster_infos
        ClusteringManager {
            clusters, // Directly use the clusters obtained from build_clusters
            embeddings,
            cluster_infos, // Use the vector populated above
        }
    }


    /// Retrieves a reference to the vector of cluster information.
    ///
    /// This method provides access to the detailed information of all clusters currently managed
    /// by the `ClusteringManager`. The information includes each cluster's points, silhouette score,
    /// and the number of clusters, encapsulated within `ClusterInfo` structs.
    ///
    /// # Returns
    /// A reference to a vector of `ClusterInfo` containing detailed information about each cluster.
    pub fn get_cluster_info(&self) -> &Vec<ClusterInfo> {
        &self.cluster_infos
    }


    /// Builds clusters based on the provided samples and configuration.
    ///
    /// This function determines the optimal number of clusters within a specified range
    /// (if given) or defaults to evaluating a preset range. It iterates over each potential
    /// cluster count, performs clustering, and collects the resulting cluster information
    /// and the clusters themselves.
    ///
    /// # Arguments
    /// * `samples` - A slice of samples represented as `f64`, used for clustering.
    /// * `n_samples` - The total number of samples provided.
    /// * `dimension` - The dimensionality of each sample.
    /// * `n_iterations` - The number of iterations to perform for each clustering attempt.
    /// * `custom_range` - An optional tuple specifying the minimum and maximum number of clusters
    ///   to consider. If `None`, a default range is used.
    ///
    /// # Returns
    /// A tuple containing two vectors:
    /// * The first vector contains `ClusterInfo` for each cluster configuration attempted,
    ///   detailing the clustering outcome.
    /// * The second vector contains `Cluster` instances representing the actual clusters formed.
    ///
    /// # Panics
    /// This function will panic if `custom_range` is `None` and the function attempts to unwrap it.
    /// Ensure `custom_range` is always `Some` when calling this function directly.
    fn build_clusters(
        samples: &[f64],
        n_samples: usize,
        dimension: usize,
        n_iterations: usize,
        custom_range: Option<(usize, usize)>,
    ) -> (Vec<ClusterInfo>, Vec<Cluster>) {
        if n_samples <= 1 {
            info!("Insufficient samples for automatic cluster determination. Using default cluster count.");
            return (Vec::new(), Vec::new());
        }

        let (min_clusters, max_clusters) = custom_range.expect("Custom range must be provided.");
        let min = std::cmp::max(2, min_clusters);
        info!("Using custom range: min={}, max={}", min, max_clusters);

        let cluster_range = (min..=max_clusters).collect::<Vec<_>>();
        info!("Initiating automatic cluster determination.");
        info!("Evaluating cluster counts from {} to {}", min, max_clusters);

        let mut cluster_infos_vec: Vec<ClusterInfo> = Vec::new();
        let mut all_clusters_vec: Vec<Cluster> = Vec::new();

        for &n_clusters in &cluster_range {
            info!("Starting clustering with {} clusters", n_clusters);

            if let Some((cluster_info, clusters)) = Self::perform_clustering(samples, n_samples, dimension, n_clusters, n_iterations) {
                cluster_infos_vec.push(cluster_info);
                all_clusters_vec.extend(clusters);
            }
        }

        (cluster_infos_vec, all_clusters_vec)
    }


    /// Performs KMeans clustering on the given dataset and calculates the silhouette score.
    ///
    /// This function attempts to cluster the given samples into a specified number of clusters
    /// using the KMeans algorithm. It catches and handles any panic that might occur during
    /// the clustering process, logging an error if clustering fails. On successful clustering,
    /// it constructs `Cluster` instances for each cluster and calculates the silhouette score
    /// for the clustering configuration. This silhouette score is a measure of how similar an
    /// object is to its own cluster compared to other clusters.
    ///
    /// # Arguments
    /// * `samples` - A slice of `f64` representing the dataset to be clustered.
    /// * `n_samples` - The number of samples in the dataset.
    /// * `dimension` - The number of features for each sample.
    /// * `n_clusters` - The desired number of clusters to form.
    /// * `n_iterations` - The number of iterations for the KMeans algorithm.
    ///
    /// # Returns
    /// An `Option` containing a tuple of `ClusterInfo` and a vector of `Cluster` instances if
    /// clustering succeeds, or `None` if an error occurs during clustering.
    fn perform_clustering(
        samples: &[f64],
        n_samples: usize,
        dimension: usize,
        n_clusters: usize,
        n_iterations: usize,
    ) -> Option<(ClusterInfo, Vec<Cluster>)> {
        let start_time = Instant::now();

        debug!("Initializing KMeans with {} samples and dimension {}", n_samples, dimension);
        let init_kmeans_time = Instant::now();
        let kmean = KMeans::new(samples.to_vec(), n_samples, dimension);
        debug!("KMeans initialization completed in {:?}", init_kmeans_time.elapsed());

        let clustering_start_time = Instant::now();
        let result = panic::catch_unwind(AssertUnwindSafe(|| {
            kmean.kmeans_lloyd(n_clusters, n_iterations, KMeans::init_kmeanplusplus, &KMeansConfig::default())
        }));
        debug!("Clustering process (kmeans_lloyd) completed in {:?}", clustering_start_time.elapsed());

        match result {
            Ok(result) => {
                debug!("Processing results and generating clusters...");
                let processing_start_time = Instant::now();

                let clusters = (0..n_clusters)
                    .map(|i| {
                        let start = i * dimension;
                        let end = start + dimension;
                        let centroid_vec: Vec<f64> = result.centroids[start..end].to_vec();
                        let centroid_array: Array1<f32> = Array1::from_vec(centroid_vec.iter().map(|&x| x as f32).collect());

                        let embeddings_indices = result.assignments.iter().enumerate()
                            .filter_map(|(idx, &cluster_idx)| {
                                if cluster_idx == i as usize { Some(idx) } else { None }
                            })
                            .collect::<Vec<usize>>();

                        Cluster {
                            centroid: centroid_array,
                            embeddings: embeddings_indices,
                        }
                    })
                    .collect::<Vec<Cluster>>();
                debug!("Cluster generation completed in {:?}", processing_start_time.elapsed());

                let silhouette_calculation_start_time = Instant::now();
                let embeddings_array2: ndarray::prelude::ArrayBase<ndarray::OwnedRepr<f32>, ndarray::prelude::Dim<[usize; 2]>> = Array2::from_shape_vec((n_samples, dimension), samples.iter().map(|&x| x as f32).collect()).unwrap();
                //let score_slow = Self::calculate_silhouette_score(&embeddings_array2, &clusters);
                let score = Self::calculate_silhouette_score_fast(&embeddings_array2, &clusters);
                
                debug!("Silhouette score calculation completed in {:?}", silhouette_calculation_start_time.elapsed());

                info!("Evaluated {} clusters: score = {:.4}, total processing completed in {} ms", n_clusters, score, start_time.elapsed().as_millis());

                let cluster_info_generation_start_time = Instant::now();
                let clusters_info = generate_cluster_info_hashmap(&clusters);
                let cluster_info = ClusterInfo {
                    cluster_points: clusters_info,
                    silhouette_score: score,
                    n_clusters: n_clusters,
                };
                debug!("ClusterInfo generation completed in {:?}", cluster_info_generation_start_time.elapsed());

                debug!("ClusterInfo and clusters ready for return.");
                Some((cluster_info, clusters))
            },
            Err(_) => {
                error!("Clustering failed for {} clusters due to an error", n_clusters);
                None
            }
        }
    }



    /// Calculates the silhouette score for a given set of embeddings and clusters.
    ///
    /// The silhouette score is a measure of how similar an object is to its own cluster (cohesion)
    /// compared to other clusters (separation). The score ranges from -1 (incorrect clustering) to
    /// 1 (highly dense clustering), where a high value indicates that the object is well matched
    /// to its own cluster and poorly matched to neighboring clusters.
    ///
    /// # Arguments
    /// * `embeddings` - A reference to an `Array2<f32>` representing the dataset's embeddings.
    /// * `clusters` - A slice of `Cluster`, representing the clusters formed from the embeddings.
    ///
    /// # Returns
    /// The average silhouette score of all samples in the dataset as a single `f32` value.
    ///
    /// # Methodology
    /// For each sample:
    /// 1. Calculate `a`: The mean distance between a sample and all other points in the same cluster.
    /// 2. Calculate `b`: The mean distance between a sample and all points in the nearest cluster
    ///    that the sample is not a part of.
    /// The silhouette score for each sample is `(b - a) / max(a, b)`.
    /// The function returns the mean silhouette score for all samples.
    fn calculate_silhouette_score(
        embeddings: &Array2<f32>,
        clusters: &[Cluster],
    ) -> f32 {
        let num_samples = embeddings.nrows();
        let mut silhouette_scores: Vec<f32> = vec![];

        // Calculate 'a' for each sample
        let mut a_values: Vec<f32> = vec![0.0; num_samples];
        for cluster in clusters {
            for &sample_idx in &cluster.embeddings {
                let other_samples = &cluster.embeddings.iter().filter(|&&i| i != sample_idx).collect::<Vec<_>>();
                let a_sum: f32 = other_samples.iter().map(|&&other_idx| {
                    euclidean_distance(&embeddings.row(sample_idx).to_owned(), &embeddings.row(other_idx).to_owned())
                }).sum();
                a_values[sample_idx] = if !other_samples.is_empty() { a_sum / other_samples.len() as f32 } else { 0.0 };
            }
        }

        // Calculate 'b' for each sample
        let mut b_values: Vec<f32> = vec![f32::MAX; num_samples];
        for (cluster_idx, cluster) in clusters.iter().enumerate() {
            for &sample_idx in &cluster.embeddings {
                for (other_cluster_idx, other_cluster) in clusters.iter().enumerate() {
                    if cluster_idx != other_cluster_idx {
                        let b_sum: f32 = other_cluster.embeddings.iter().map(|&other_idx| {
                            euclidean_distance(&embeddings.row(sample_idx).to_owned(), &embeddings.row(other_idx).to_owned())
                        }).sum();
                        let b_mean = b_sum / other_cluster.embeddings.len() as f32;
                        b_values[sample_idx] = b_values[sample_idx].min(b_mean);
                    }
                }
            }
        }

        // Compute silhouette score for each sample and calculate the average
        for i in 0..num_samples {
            let a = a_values[i];
            let b = b_values[i];
            let score = if a < b { (b - a) / b.max(a) } else { 0.0 };
            silhouette_scores.push(score);
        }

        silhouette_scores.iter().sum::<f32>() / num_samples as f32
    }


    /// Calculates the silhouette score for a subset of the dataset's embeddings and clusters, aiming for faster execution.
    ///
    /// This function aims to approximate the silhouette score by utilizing parallel computation and SIMD instructions
    /// for distance calculations. The silhouette score provides insight into the clustering quality, measuring how 
    /// similar an object is to its own cluster (cohesion) versus other clusters (separation). The score ranges from 
    /// -1 (indicating incorrect clustering) to 1 (indicating very dense clustering). A higher score suggests that 
    /// objects are well matched to their own cluster and distinct from neighboring clusters.
    ///
    /// # Arguments
    /// * `embeddings` - A reference to an `Array2<f32>` representing the dataset's embeddings. This array should 
    /// contain the data points in a 2D layout where each row corresponds to a data point's features.
    /// * `clusters` - A slice of `Cluster`, representing the clusters formed from the embeddings. Each `Cluster` 
    /// should contain a centroid and the indices of embeddings belonging to the cluster.
    ///
    /// # Returns
    /// The average silhouette score of the sampled data points as a single `f32` value. This score is computed 
    /// by calculating the mean silhouette score across the sampled points, thereby providing an approximation 
    /// of the overall clustering quality.
    ///
    /// # Methodology
    /// The function executes in two main steps for each sampled data point:
    /// 1. Calculate `a`: The mean distance between a sample and all other points in the same cluster, leveraging 
    /// parallel processing and SIMD for efficiency.
    /// 2. Calculate `b`: The mean distance between a sample and all points in the nearest cluster that the sample 
    /// is not a part of, again using parallel processing and SIMD for fast execution.
    /// The silhouette score for each sampled data point is then computed as `(b - a) / max(a, b)`, and the function
    /// returns the mean silhouette score across all sampled points.
    ///
    /// # Sample Selection
    /// This function assumes that the sampling of data points to calculate the silhouette score for has already 
    /// been determined by the caller or occurs within the clustering process, allowing for a focused and faster 
    /// approximation of the silhouette score across a representative subset of the dataset.
    pub fn calculate_silhouette_score_fast(embeddings: &Array2<f32>, clusters: &[Cluster]) -> f32 {
        let num_samples = embeddings.nrows();
    
        // Parallel calculation of 'a' values
        let a_values: Vec<f32> = (0..num_samples).into_par_iter().map(|sample_idx| {
            clusters.iter()
                .find(|cluster| cluster.embeddings.contains(&sample_idx))
                .map(|cluster| {
                    cluster.embeddings.par_iter()
                        .filter(|&&i| i != sample_idx)
                        .map(|&other_idx| unsafe {
                            // Assuming simd_distance can be safely called
                            simd_distance(&embeddings.row(other_idx).to_owned().into(), &embeddings.row(sample_idx).to_owned().into())
                        })
                        .collect::<Vec<f32>>()
                })
                .map_or(0.0, |distances| {
                    if !distances.is_empty() {
                        distances.iter().sum::<f32>() / distances.len() as f32
                    } else {
                        0.0
                    }
                })
        }).collect();
    
        // Parallel calculation of 'b' values
        let b_values: Vec<f32> = (0..num_samples).into_par_iter().map(|sample_idx| {
            clusters.iter()
                .filter(|cluster| !cluster.embeddings.contains(&sample_idx))
                .map(|other_cluster| {
                    other_cluster.embeddings.par_iter()
                        .map(|&other_idx| unsafe {
                            // Assuming simd_distance can be safely called
                            simd_distance(&embeddings.row(other_idx).to_owned().into(), &embeddings.row(sample_idx).to_owned().into())
                        })
                        .collect::<Vec<f32>>()
                })
                .filter_map(|distances| if !distances.is_empty() { Some(distances.iter().sum::<f32>() / distances.len() as f32) } else { None })
                .min_by(|a, b| a.partial_cmp(b).unwrap())
                .unwrap_or(f32::MAX)
        }).collect();
    
        // Compute silhouette scores and their average
        a_values.into_par_iter().zip(b_values.into_par_iter())
            .map(|(a, b)| {
                if a < b {
                    (b - a) / b.max(a)
                } else {
                    0.0
                }
            })
            .sum::<f32>() / num_samples as f32
    }

    

    /// Finds the indices of the nearest centroids to a given query embedding.
    ///
    /// This function computes the Euclidean distance between the query embedding and each centroid
    /// in the dataset. It then returns the indices of the `top_c` closest centroids based on these
    /// distances. This is useful for identifying which clusters are most relevant to a given data point.
    ///
    /// # Arguments
    /// * `query_embedding` - A reference to an `Array1<f32>` representing the query embedding.
    /// * `top_c` - The number of closest centroids to return.
    ///
    /// # Returns
    /// A vector of indices corresponding to the nearest centroids, sorted by increasing distance
    /// from the query embedding. The length of the vector is determined by `top_c`.
    ///
    /// # Example
    /// Given a query embedding and a desire to find the three nearest centroids:
    /// ```
    /// let nearest_centroids = clustering_manager.find_nearest_centroids(query_embedding, 3);
    /// ```
    /// This will return the indices of the three closest centroids to the query embedding.
    pub fn find_nearest_centroids(&self, query_embedding: &Array1<f32>, top_c: usize) -> Vec<usize> {
        debug!("Finding nearest centroids using Euclidean distance.");

        // Calculate the distance between the query embedding and each centroid
        let distances: Vec<_> = self.clusters.iter().enumerate().map(|(idx, cluster)| {
            let distance = cluster.centroid.iter().zip(query_embedding.iter())
                .map(|(a, b)| (a - b).powi(2))
                .sum::<f32>()
                .sqrt();
            (idx, distance)
        }).collect();

        // Sort the indices of distances in increasing order based on the calculated distances
        let mut distance_indices: Vec<_> = distances.iter().enumerate().map(|(idx, _)| idx).collect();
        distance_indices.sort_by(|&a, &b| distances[a].1.partial_cmp(&distances[b].1).unwrap_or(Ordering::Equal));

        // Return the indices of the top_c nearest centroids
        distance_indices.into_iter().map(|idx| distances[idx].0).take(top_c).collect()
    }


    /// Aggregates similarity or distance scores for embeddings from the nearest clusters to a query embedding.
    ///
    /// This function calculates the similarity (using cosine similarity) or distance (using Euclidean distance)
    /// between a query embedding and all embeddings in the nearest clusters identified by their indices.
    /// It aggregates these results and returns the top N results sorted by their similarity or distance score.
    ///
    /// # Arguments
    /// * `nearest_centroids` - A vector of indices for the nearest centroids to the query embedding.
    /// * `query_embedding` - A reference to the query embedding as an `Array1<f32>`.
    /// * `top_n` - The number of top results to return based on the highest similarity or lowest distance.
    ///
    /// # Returns
    /// A vector of tuples, each containing an embedding index and its corresponding similarity or distance score,
    /// sorted in descending order of similarity or ascending order of distance.
    ///
    /// # Note
    /// The function uses cosine similarity by default to measure similarity. Set `use_cosine_similarity` to `false`
    /// to use Euclidean distance instead.
    pub fn aggregate_results_from_clusters(&self, nearest_centroids: Vec<usize>, query_embedding: &Array1<f32>, top_n: usize) -> Vec<(usize, f32)> {
        debug!("Aggregating results from clusters.");

        let use_cosine_similarity = true; // Toggle to false to use Euclidean distance instead of cosine similarity
        let query_embedding_arc = Arc::new(query_embedding.clone());

        // Declare `all_results` as mutable to allow sorting
        let mut all_results: Vec<(usize, f32)> = nearest_centroids.par_iter().flat_map(|&cluster_idx| {
            let cluster = &self.clusters[cluster_idx];
            if cluster.embeddings.is_empty() {
                debug!("Cluster {} has zero embeddings.", cluster_idx);
                return Vec::new(); // Skip clusters with no embeddings
            }
            let query_embedding_clone = Arc::clone(&query_embedding_arc);

            cluster.embeddings.par_iter().map(move |&emb_idx| {
                let emb = self.embeddings.row(emb_idx).to_owned();
                let similarity_or_distance = if use_cosine_similarity {
                    cosine_similarity(&emb, &query_embedding_clone)
                } else {
                    // Invert Euclidean distance to ensure higher values indicate closer or more similar items
                    1.0 / (1.0 + euclidean_distance(&emb, &query_embedding_clone))
                };

                (emb_idx, similarity_or_distance)
            }).collect::<Vec<(usize, f32)>>()
        }).collect();

        // Now `all_results` can be sorted in place because it's mutable
        all_results.par_sort_unstable_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(Ordering::Equal));

        debug!("Sorting aggregated results by similarity/distance.");
        all_results.into_iter().take(top_n).collect()
    }


}