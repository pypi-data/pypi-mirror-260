//lib.rs

// Import necessary crates for Python bindings, asynchronous runtime, logging, and data manipulation.
use pyo3::prelude::*;
use std::collections::HashMap;
use rayon::prelude::*;
use log::{info, warn, debug, error};
use ndarray::{Array1, Array2};
use std::time::Instant;
use serde::{Serialize, Deserialize};
use std::fs::{File, OpenOptions};
use std::io::Write;
use memmap2::{MmapMut, MmapOptions};
use env_logger::{Builder, Env};
use log::LevelFilter;
use chrono::Local;
use serde_json::{self, json};
use std::cmp::Ordering;
use tokio::runtime::Runtime;
use anyhow::{anyhow, Error};
//use std::env;


// Declare module-level imports for organizational purposes.
mod utils;
mod clustering;
mod recal;
mod memory;
mod vertex_embeddings;

/// Enumerates the types of return values supported by certain operations.
enum ReturnType {
    Id,
    Vector,
    Content,
    Full,
}



/// Represents an embedding with associated content and metadata.
#[pyclass]
#[derive(Serialize, Deserialize, Clone)]
pub struct Embedding {
    id: String,
    content: String,
    embedding: Vec<f32>,
    metadata: HashMap<String, String>,
}

/// Manages embeddings, providing functionality for adding, updating, deleting, and searching.
#[pyclass]
pub struct EmbeddingManager {
    embeddings: HashMap<String, Vec<f32>>,
    metadata: HashMap<String, (String, HashMap<String, String>)>,
    clustering_manager: Option<clustering::ClusteringManager>,
    cluster_out_of_date: bool,
}

#[pymethods]
impl EmbeddingManager {
    /// Constructs a new `EmbeddingManager`.
    /// This manager handles embeddings and associated metadata, and can optionally pre-allocate
    /// capacity for efficiency. It supports clustering operations, although clustering must be
    /// manually initialized and marked when out of date.
    ///
    /// # Parameters
    /// - `capacity`: Optional. Pre-allocates space for the embeddings HashMap if Some.
    #[new]
    fn new(capacity: Option<usize>) -> Self {
        let embeddings: HashMap<String, Vec<f32>> = match capacity {
            Some(cap) => {
                debug!("Initializing EmbeddingManager with capacity: {}", cap);
                HashMap::with_capacity(cap)
            },
            None => {
                debug!("Initializing EmbeddingManager without specified capacity.");
                HashMap::new()
            },
        };

        Self {
            embeddings,
            metadata: HashMap::new(), // Stores additional metadata for embeddings.
            clustering_manager: None, // Optional clustering manager, not initialized by default.
            cluster_out_of_date: false, // Tracks if clustering needs to be updated.
        }
    }

    /// Initializes the vertex embedding environment.
    /// This function sets up the necessary runtime and calls an asynchronous initialization
    /// routine for the vertex embeddings. It is designed to be called with Python interop in mind,
    /// taking advantage of PyO3's capabilities for Rust-Python integration.
    ///
    /// # Parameters
    /// - `_py`: Python interpreter handle, used for error handling in Python context.
    /// - `project_id`: The unique identifier for the project for which embeddings are to be initialized.
    /// - `location`: The location identifier where the embeddings service is deployed.
    /// - `qps`: Specifies the Queries Per Second (QPS) limit for the embedding service, used for rate limiting.
    ///
    /// # Returns
    /// - `PyResult<()>`: Returns `Ok(())` if the initialization is successful, or a Python runtime error if an error occurs.
    pub fn init_vertex_embedding(&self, _py: Python, project_id: String, location: String, qps: u64) -> PyResult<()> {
        // Log the beginning of the initialization process. This could be helpful for debugging and monitoring.
        // e.g., info!("Initializing vertex embedding for project_id: {}, location: {}, with QPS: {}", project_id, location, qps);
        
        let rt = Runtime::new().unwrap(); // Consider handling this potential panic more gracefully in future revisions.
        rt.block_on(async {
            vertex_embeddings::v_init(&project_id, &location, qps)
                .map_err(|e| {
                    // Log the error before returning it to Python for additional context in Rust logs.
                    // e.g., error!("Failed to initialize vertex embedding: {}", e);
                    pyo3::exceptions::PyRuntimeError::new_err(format!("Failed to initialize vertex embedding: {}", e))
                })
        })
    }


    /// Generates an embedding for the given content using Vertex AI based on the specified mode
    /// and manages it within the embedding manager. This can involve either loading the embedding
    /// into the manager or retrieving it directly.
    ///
    /// # Parameters
    /// - `_py`: Python interpreter handle for error handling.
    /// - `id`: Unique identifier for the embedding.
    /// - `title`: The title of the content to embed.
    /// - `content`: The actual content to embed.
    /// - `metadata`: Additional metadata associated with the embedding.
    /// - `mode_str`: Operation mode, either "load" for adding the embedding to the manager,
    ///   or "retrieve" for fetching the embedding without storing it.
    ///
    /// # Returns
    /// - `PyResult<Option<Vec<f32>>>`: Returns `None` when loading an embedding (as the embedding is stored),
    ///   or `Some(Vec<f32>)` with the embedding vector when retrieving. Returns a Python runtime error on failure.
    pub fn vertex_embedding(&mut self, _py: Python, id: String, title: String, content: String, metadata: HashMap<String, String>, mode_str: &str) -> PyResult<Option<Vec<f32>>> {
        // Log start of the embedding operation
        debug!("Starting vertex embedding operation for ID: {}, mode: {}", id, mode_str);
        
        let rt = Runtime::new().unwrap(); // Note: Consider error handling for production use.
        let result: Result<Option<Vec<f32>>, Error> = rt.block_on(async {
            match vertex_embeddings::fetch_embeddings(&title, &content, mode_str).await {
                Ok(embedding_values) => {
                    match mode_str {
                        "load" => {
                            debug!("Loading embedding for ID: {}", id);
                            self.add_embedding(id, content, embedding_values.clone(), metadata);
                            Ok(None)
                        },
                        "retrieve" => {
                            debug!("Retrieving embedding for ID: {}", id);
                            Ok(Some(embedding_values))
                        },
                        _ => Err(anyhow!("Invalid operation mode specified").into()),
                    }
                },
                Err(e) => {
                    // Log fetch_embeddings error
                    error!("Error fetching embeddings: {}", e);
                    Err(e.into())
                },
            }
        });
        result.map_err(|e| {
            // Log before returning error to Python
            error!("Failed to execute vertex embedding operation: {}", e);
            pyo3::exceptions::PyRuntimeError::new_err(format!("Failed to execute vertex embedding: {}", e))
        })
    }


    /// Adds a new embedding to the manager, updating relevant data structures. If an embedding
    /// with the same ID already exists, it is overwritten, and a warning is logged. This operation
    /// also marks the clustering as out of date, indicating that re-clustering may be necessary.
    ///
    /// # Parameters
    /// - `id`: Unique identifier for the embedding.
    /// - `content`: Content associated with the embedding.
    /// - `embedding`: The embedding vector.
    /// - `metadata`: Metadata associated with the embedding.
    fn add_embedding(&mut self, id: String, content: String, embedding: Vec<f32>, metadata: HashMap<String, String>) {
        // Check if the embedding already exists to log appropriately without unnecessary cloning.
        let existing = self.embeddings.insert(id.clone(), embedding);
        self.metadata.insert(id.clone(), (content, metadata));
        self.cluster_out_of_date = true;

        debug!("Added embedding with ID: {}", id);
        if existing.is_some() {
            // Log a warning if an existing embedding was overwritten.
            warn!("Overwrote existing embedding with ID: {}. Clustering data marked as out of date.", id);
        } else {
            debug!("Clustering data marked as out of date due to new embedding addition.");
        }
    }


    /// Adds multiple embeddings to the manager in bulk. Each embedding is defined by a tuple
    /// containing an ID, content, embedding vector, and metadata. This method optimizes for
    /// performance by reserving space in the data structures upfront and marks the clustering
    /// as out of date upon completion.
    ///
    /// # Parameters
    /// - `embeddings`: A vector of tuples, each containing an ID (String), content (String),
    ///   embedding vector (Vec<f32>), and metadata (HashMap<String, String>).
    fn add_embeddings_bulk(&mut self, embeddings: Vec<(String, String, Vec<f32>, HashMap<String, String>)>) {
        info!("Starting bulk addition of embeddings. Total embeddings to add: {}", embeddings.len());
        self.embeddings.reserve(embeddings.len());
        self.metadata.reserve(embeddings.len());

        for (id, content, embedding, metadata) in embeddings {
            // Check if an embedding is being overwritten, which could be important for debugging.
            if let Some(_) = self.embeddings.insert(id.clone(), embedding) {
                debug!("Overwrote existing embedding with ID: {}", id);
            }
            self.metadata.insert(id, (content, metadata));
        }

        self.cluster_out_of_date = true;
        info!("Completed bulk addition of embeddings.");
    }


    /// Updates an existing embedding and/or its metadata based on provided options. If either
    /// new_embedding or new_metadata is Some, the corresponding data for the ID is updated.
    /// The clustering is marked as out of date if any updates occur.
    ///
    /// # Parameters
    /// - `id`: The unique identifier for the embedding to update.
    /// - `new_embedding`: Optional new embedding vector to replace the existing one.
    /// - `new_metadata`: Optional new metadata to replace the existing metadata.
    fn update_embedding(&mut self, id: &str, new_embedding: Option<Vec<f32>>, new_metadata: Option<HashMap<String, String>>) {
        let mut updated = false;

        // Log the attempt to update to provide context for debugging.
        debug!("Attempting to update embedding and/or metadata for ID: {}", id);

        if let Some(emb) = new_embedding {
            self.embeddings.insert(id.to_string(), emb);
            info!("Updated embedding vector for ID: {}", id);
            updated = true;
        }

        if let Some(meta) = new_metadata {
            if self.metadata.get_mut(id).map(|e| e.1 = meta).is_some() {
                info!("Updated metadata for ID: {}", id);
                updated = true;
            } else {
                warn!("Attempted to update metadata for non-existent ID: {}", id);
            }
        }

        if updated {
            self.cluster_out_of_date = true;
            info!("Marked clustering as out of date due to updates.");
        } else {
            // Log if no updates occurred for clarity.
            debug!("No updates made for ID: {}", id);
        }
    }


    /// Deletes an embedding and its associated metadata from the manager, if they exist.
    /// This operation also marks the clustering as out of date, indicating that the overall
    /// clustering might need reevaluation due to the change in data.
    ///
    /// # Parameters
    /// - `id`: The unique identifier for the embedding and metadata to be deleted.
    fn delete_embedding(&mut self, id: &str) {
        let removed_embedding = self.embeddings.remove(id);
        let removed_metadata = self.metadata.remove(id);

        if removed_embedding.is_some() && removed_metadata.is_some() {
            info!("Deleted both embedding and metadata for ID: {}", id);
        } else if removed_embedding.is_some() {
            info!("Deleted embedding for ID: {} but found no associated metadata.", id);
        } else if removed_metadata.is_some() {
            info!("Deleted metadata for ID: {} but found no associated embedding.", id);
        } else {
            warn!("Attempted to delete non-existent embedding and metadata with ID: {}", id);
        }

        self.cluster_out_of_date = true;
    }


    /// Retrieves an embedding by its ID, along with its content and metadata, if available.
    /// Returns a tuple containing the content (String), embedding vector (Vec<f32>),
    /// and metadata (HashMap<String, String>). Returns None if the embedding or metadata
    /// is not found for the given ID.
    ///
    /// # Parameters
    /// - `id`: The unique identifier for the embedding to retrieve.
    ///
    /// # Returns
    /// - `PyResult<Option<(String, Vec<f32>, HashMap<String, String>)>>`: The embedding data if found, or None.
    fn get_embedding_by_id(&self, id: &str) -> PyResult<Option<(String, Vec<f32>, HashMap<String, String>)>> {
        match (self.embeddings.get(id), self.metadata.get(id)) {
            (Some(embedding), Some((content, metadata))) => {
                info!("Retrieved embedding for ID: {}. Size: {}", id, embedding.len());
                Ok(Some((content.clone(), embedding.clone(), metadata.clone())))
            }
            _ => {
                debug!("No embedding found for ID: {}", id);
                Ok(None)
            }
        }
    }


    /// Performs a brute force search to find the top N closest embeddings to a given query embedding.
    /// 
    /// This function computes the cosine similarity between a query embedding and all embeddings stored,
    /// sorting them to return the top N closest matches. The type of data returned for each match can be
    /// specified through `return_type_str`.
    ///
    /// # Parameters
    /// - `query_embedding`: The query embedding as a vector of f32.
    /// - `top_n`: The number of top closest embeddings to return.
    /// - `return_type_str`: A string specifying the type of data to return for each embedding. Can be "id",
    ///   "vector", "content", or "full" for different levels of detail.
    ///
    /// # Returns
    /// - `PyResult<Vec<(String, Option<Vec<f32>>, Option<String>, f32)>>`: A vector of tuples, each containing
    ///   the ID, optional embedding vector, optional content and metadata JSON, and the cosine similarity score.
    ///
    /// # Errors
    /// - Returns an error if an invalid `return_type_str` is specified.
    fn brute_force_search(&self, query_embedding: Vec<f32>, top_n: usize, return_type_str: String) -> PyResult<Vec<(String, Option<Vec<f32>>, Option<String>, f32)>> {
        let start_time = Instant::now();
        // Log the start of a brute force search with the number of top N closest embeddings to find.
        info!("Starting brute force search for the top {} closest embeddings.", top_n);

        let return_type = match return_type_str.as_str() {
            "id" => ReturnType::Id,
            "vector" => ReturnType::Vector,
            "content" => ReturnType::Content,
            "full" => ReturnType::Full,
            _ => {
                // Warn if an invalid return type is specified and return an error.
                warn!("Invalid return type specified: {}", return_type_str);
                return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid return type"));
            }
        };

        let similarities: Vec<_> = self.embeddings
            .par_iter()
            .map(|(id, emb)| {
                let similarity = utils::cosine_similarity(emb, &query_embedding);
                let content_opt = self.metadata.get(id).map(|(content, _)| content.clone());
                let metadata_opt = self.metadata.get(id).map(|(_, metadata)| serde_json::to_string(metadata).unwrap_or_default());

                let combined_content_metadata = match return_type {
                    ReturnType::Content | ReturnType::Full => json!({
                        "content": content_opt,
                        "metadata": metadata_opt.map_or_else(|| json!({}), |m| serde_json::from_str(&m).unwrap_or_default())
                    }).to_string(),
                    _ => content_opt.unwrap_or_default(),
                };

                (id.clone(), Some(emb.clone()), Some(combined_content_metadata), similarity)
            })
            .collect();

        let mut sorted_similarities = similarities;
        sorted_similarities.sort_by(|a, b| b.3.partial_cmp(&a.3).unwrap_or(Ordering::Equal));

        let results: Vec<_> = sorted_similarities
            .into_iter()
            .take(top_n)
            .map(|(id, emb, combined_content_metadata, similarity)| {
                match return_type {
                    ReturnType::Id => (id, None, None, similarity),
                    ReturnType::Vector => (id, emb, None, similarity),
                    ReturnType::Content  => (id, None, combined_content_metadata, similarity),
                    ReturnType::Full => (id, emb, combined_content_metadata, similarity),
                }
            })
            .collect();

        let total_duration = start_time.elapsed();
        // Log the completion of the brute force search including the total duration.
        info!("Brute force search completed in {} ms.", total_duration.as_millis());

        Ok(results)
    }

    /// Initializes and performs K-means clustering on the embeddings stored in `self.embeddings`,
    /// creating `n_clusters` clusters through `n_iterations` iterations of the algorithm.
    ///
    /// # Parameters
    /// - `n_clusters`: The number of clusters to create, as an isize.
    /// - `n_iterations`: The number of iterations for the K-means clustering algorithm, as usize.
    ///
    /// # Returns
    /// - `PyResult<String>`: On success, returns a JSON string representing the cluster information.
    ///   On failure, returns a Python error.
    ///
    /// # Example
    /// ```
    /// let mut clustering_instance = ClusteringInstance::new();
    /// let result = clustering_instance.create_clusters(5, 100);
    /// if let Ok(json_string) = result {
    ///     println!("Cluster info: {}", json_string);
    /// }
    /// ```
    fn create_clusters(&mut self, n_clusters: isize, n_iterations: usize) -> PyResult<String> {
        let start_time = Instant::now();
        // Log the start of the clustering process with the specified number of clusters.
        info!("Initializing clustering process for {} clusters.", n_clusters);
        
        // Convert the embeddings stored in the hashmap to an ndarray format for processing.
        let embeddings_matrix: Array2<f32> = utils::hashmap_to_ndarray(&self.embeddings);
        // Log the time taken to convert embeddings to ndarray format.
        info!("Conversion of embeddings to ndarray format completed in {} ms.", start_time.elapsed().as_millis());
        
        // Initialize the clustering manager with the embeddings matrix, number of clusters, and iterations.
        let clustering_manager = clustering::ClusteringManager::new(embeddings_matrix, n_clusters, n_iterations);
        // Log the completion of the K-means clustering process.
        info!("K-means clustering process completed in {} ms.", start_time.elapsed().as_millis());
        
        // Update the instance's clustering manager and mark the cluster data as up-to-date.
        self.clustering_manager = Some(clustering_manager);
        self.cluster_out_of_date = false;
        
        // Retrieve the cluster information from the clustering manager for serialization.
        debug!("Retrieving cluster info from clustering_manager.");
        let cluster_infos = self.clustering_manager.as_ref().unwrap().get_cluster_info();

        // Serialize the cluster information into a JSON string.
        debug!("Serializing cluster info to JSON string.");
        let json_string = serde_json::to_string(&cluster_infos)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Failed to serialize cluster info: {}", e)))?;
        // Log the successful serialization of the cluster information.
        debug!("Serialized cluster info JSON string: {}", json_string);

        // Return the serialized JSON string containing the cluster information.
        Ok(json_string)
    }

    /// Performs a search for the top N closest embeddings to a given query embedding using clustering.
    /// This function first finds the nearest centroids to the query embedding, then aggregates results
    /// from those clusters to find the top N closest embeddings.
    ///
    /// # Parameters
    /// - `query_embedding`: The query embedding as a Vec<f32>.
    /// - `top_c`: The number of top closest centroids to consider in the search.
    /// - `top_n`: The number of top closest embeddings to return.
    /// - `return_type_str`: Specifies the type of data to return ("id", "vector", "content", or "full").
    /// - `force_search`: If true, forces the search even if the clustering information is out of date.
    ///
    /// # Returns
    /// - `PyResult<Vec<(String, Option<Vec<f32>>, Option<String>, f32)>>`: A vector of tuples, each
    ///   containing an embedding ID, an optional vector, optional content and metadata as a JSON string,
    ///   and the similarity score.
    ///
    /// # Errors
    /// - Returns an error if an invalid return type is specified.
    /// - Returns a vector with a single error message tuple if clustering information is out of date
    ///   and `force_search` is false.
    fn cluster_search(&self, query_embedding: Vec<f32>, top_c: usize, top_n: usize, return_type_str: String, force_search: bool) -> PyResult<Vec<(String, Option<Vec<f32>>, Option<String>, f32)>> {
        let total_start = Instant::now();
        info!("Starting cluster-based search.");

        let return_type = match return_type_str.as_str() {
            "id" => ReturnType::Id,
            "vector" => ReturnType::Vector,
            "content" => ReturnType::Content,
            "full" => ReturnType::Full,
            _ => {
                warn!("Invalid return type specified: {}", return_type_str);
                return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid return type"));
            }
        };

        if self.cluster_out_of_date && !force_search {
            warn!("Cluster-based search attempted with outdated clustering information.");
            return Ok(vec![("Cluster is out of date. Consider using brute_force_search or re-clustering.".to_string(), None, None, -1.0)]);
        }

        let clustering_manager = self.clustering_manager.as_ref().expect("Clusters not initialized");
        let query_array = Array1::from_vec(query_embedding);
        let nearest_centroids = clustering_manager.find_nearest_centroids(&query_array, top_c);
        debug!("Nearest centroids found: {:?}", nearest_centroids);

        let results = clustering_manager.aggregate_results_from_clusters(nearest_centroids, &query_array, top_n);
        let id_results: Vec<_> = results
            .iter()
            .filter_map(|(idx, similarity)| {
                let id = self.embeddings.keys().nth(*idx)?.clone();
                let vector = if matches!(return_type, ReturnType::Vector | ReturnType::Full) {
                    Some(self.embeddings.get(&id)?.clone())
                } else {
                    None
                };
                let content_metadata = if matches!(return_type, ReturnType::Content | ReturnType::Full) {
                    let content = self.metadata.get(&id)?.0.clone();
                    let metadata = &self.metadata.get(&id)?.1;
                    let combined = json!({
                        "content": content,
                        "metadata": metadata
                    });
                    Some(serde_json::to_string(&combined).unwrap_or_default())
                } else {
                    None
                };
                Some((id, vector, content_metadata, *similarity))
            })
            .collect();

        info!("Cluster-based search completed in {} ms.", total_start.elapsed().as_millis());
        Ok(id_results)
    }

    /// Exposes the recall test function to Python, performing a recall test based on the provided parameters.
    /// This function calculates the recall score by comparing the top N results from a cluster search
    /// against a brute force search for a subset of the embeddings.
    ///
    /// # Parameters
    /// - `test_percentage`: The percentage of the dataset to use for testing, as usize.
    /// - `top_c`: The number of top closest centroids to consider in the cluster search.
    /// - `top_n`: The number of top results to compare for calculating the recall score.
    ///
    /// # Returns
    /// - `PyResult<f32>`: The calculated recall score as a floating-point number.
    ///   On success, returns the recall score. On failure, returns a Python error.
    ///
    /// # Example
    /// ```
    /// let recall_score = instance.recal_test(10, 5, 10)?;
    /// println!("Recall score: {}", recall_score);
    /// ```
    fn recal_test(&self, test_percentage: usize, top_c: usize, top_n: usize) -> PyResult<f32> {
        // Log the initiation of the recall test along with the parameters for transparency and debugging purposes.
        info!("Starting recall test with test_percentage: {}, top_c: {}, top_n: {}.", test_percentage, top_c, top_n);

        // Invoke the recall test function from the recal module with the provided parameters.
        let recall_score = recal::recal_test(self, test_percentage, top_c, top_n);

        // Log the completion of the recall test and the calculated recall score for monitoring and analysis.
        info!("Recall test completed. Recall score: {:.4}", recall_score);

        // Return the calculated recall score.
        Ok(recall_score)
    }

    // Load embeddings from a file
    pub fn load_from_file(&mut self) -> PyResult<()> {
        let file = File::open("embeddings.dat")
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("{}", e)))?;
        let mmap = unsafe { MmapOptions::new().map(&file) }
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("{}", e)))?;
        let embeddings: Vec<Embedding> = serde_json::from_slice(&mmap)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("{}", e)))?;

        // Clear current embeddings and metadata before populating from loaded data.
        self.embeddings.clear();
        self.metadata.clear();

        // Populate embeddings and metadata from loaded data.
        for embedding in embeddings {
            self.embeddings.insert(embedding.id.clone(), embedding.embedding.clone());
            self.metadata.insert(embedding.id.clone(), (embedding.content.clone(), embedding.metadata.clone()));
        }

        Ok(())
    }

    /// Saves the current embeddings and their metadata to a file named `embeddings.dat`.
    ///
    /// This function serializes the embeddings and metadata to a JSON format and writes them
    /// to the file, using memory mapping for efficient file I/O operations. If the file does not
    /// exist, it is created. If it does exist, its contents are replaced.
    ///
    /// # Returns
    /// - `PyResult<()>`: Ok(()) if successful, or a Python exception on error.
    pub fn save_to_file(&self) -> PyResult<()> {
        let embeddings: Vec<Embedding> = self.embeddings.iter().map(|(id, embedding)| {
            let content = self.metadata.get(id).map_or(String::new(), |(content, _)| content.clone());
            let metadata = self.metadata.get(id).map_or(HashMap::new(), |(_, metadata)| metadata.clone());
            Embedding {
                id: id.clone(),
                content,
                embedding: embedding.clone(),
                metadata,
            }
        }).collect();

        let serialized_data = serde_json::to_vec(&embeddings)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("{}", e)))?;

        let file = OpenOptions::new()
            .read(true)
            .write(true)
            .create(true)
            .open("embeddings.dat")
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("{}", e)))?;

        file.set_len(serialized_data.len() as u64)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("{}", e)))?;

        let mut mmap = unsafe { MmapMut::map_mut(&file) }
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("{}", e)))?;

        mmap[..serialized_data.len()].copy_from_slice(&serialized_data);
        mmap.flush()
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("{}", e)))?;

        Ok(())
    }
}

/// Initializes the `rust_embeddings` Python module, setting up environment-specific logging and adding
/// the `EmbeddingManager` class to the module.
#[pymodule]
fn rustvdb(_py: Python, m: &PyModule) -> PyResult<()> {
    // Setup the filename for logging with a timestamp.
    let timestamp = Local::now().format("%Y-%m-%dT%H-%M-%S").to_string();
    let filename = format!("./rustvecdb_log_{}.txt", timestamp);

    // Attempt to create the log file, handling errors gracefully.
    let log_file = File::create(&filename)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("Failed to create log file {}: {}", filename, e)))?;

    // Initialize the logger with a custom format and filter level.
    Builder::from_env(Env::default().default_filter_or("info")) // Use environment variable to set default log level, fallback to "info".
        .format(|buf, record| {
            writeln!(
                buf,
                "{} [{}] - {}: {}",
                Local::now().format("%Y-%m-%d %H:%M:%S"),
                record.target(),
                record.level(),
                record.args()
            )
        })
        .target(env_logger::Target::Pipe(Box::new(log_file)))
        .init();

    // Add the EmbeddingManager class to the Python module, ensuring it's ready for Python integration.
    m.add_class::<EmbeddingManager>()?;

    Ok(())
}
