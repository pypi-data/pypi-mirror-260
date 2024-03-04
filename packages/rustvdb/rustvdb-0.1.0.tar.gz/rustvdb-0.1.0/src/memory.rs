//memory.rs

use memmap2::{MmapMut, MmapOptions};
use serde::{Serialize, Deserialize};
use serde_json;
use std::collections::HashMap;
use std::fs::{File, OpenOptions};
use std::io::{Result, Error, ErrorKind};
use std::path::Path;

#[derive(Serialize, Deserialize, Clone)]
pub struct Embedding {
    pub id: String,
    pub content: String,
    pub embedding: Vec<f32>,
    pub metadata: HashMap<String, String>,
}

/// Saves a vector of `Embedding` instances to a specified file using memory mapping.
///
/// This function serializes the vector into JSON and writes it to a file. If the file does not exist,
/// it will be created. The function uses memory mapping for efficient file writing.
///
/// # Arguments
///
/// * `embeddings` - A reference to a vector of `Embedding` instances to be saved.
/// * `file_path` - A reference to the `Path` where the embeddings should be saved.
///
/// # Returns
///
/// A `Result` indicating success (`Ok(())`) or containing an `io::Error` if an error occurred.
///
/// # Errors
///
/// This function can return an `Error` in several cases, including but not limited to:
/// - Serialization failure (if the embeddings vector cannot be serialized into JSON).
/// - File opening failure (if the file specified by `file_path` cannot be opened or created).
/// - File write failure (if the data cannot be written to the file).
///
/// # Examples
///
/// ```no_run
/// let embeddings = vec![
///     Embedding {
///         id: "1".to_string(),
///         content: "example content".to_string(),
///         embedding: vec![0.1, 0.2, 0.3],
///         metadata: HashMap::new(),
///     },
/// ];
/// let file_path = Path::new("embeddings.json");
/// save_embeddings_to_file(&embeddings, file_path).expect("Failed to save embeddings");
/// ```
pub fn save_embeddings_to_file(embeddings: &Vec<Embedding>, file_path: &Path) -> Result<()> {
    // Serialize the embeddings vector to a JSON string
    let serialized_data = serde_json::to_vec(&embeddings)
        .map_err(|e| Error::new(ErrorKind::Other, e.to_string()))?;

    // Open or create the file to memory-map
    let file = OpenOptions::new()
        .read(true)
        .write(true)
        .create(true)
        .open(file_path)?;

    // Ensure the file is large enough to hold your data
    file.set_len(serialized_data.len() as u64)?;

    // Create a memory-mapped file
    let mut mmap = unsafe { MmapMut::map_mut(&file)? };

    // Write data to the memory-mapped file
    mmap[..serialized_data.len()].copy_from_slice(&serialized_data);

    // Flush changes to ensure data is written to the file system
    mmap.flush()?;
    Ok(())
}


/// Loads a vector of `Embedding` instances from a specified file using memory mapping.
///
/// This function opens the specified file, memory-maps it for efficient access, and
/// deserializes its JSON content into a vector of `Embedding` instances.
///
/// # Arguments
///
/// * `file_path` - A reference to the `Path` where the embeddings are saved.
///
/// # Returns
///
/// A `Result` containing either a vector of `Embedding` instances or an `io::Error`.
///
/// # Errors
///
/// This function can return an `Error` in several cases, including but not limited to:
/// - File not found (if the file specified by `file_path` does not exist).
/// - File open failure (if the file cannot be opened).
/// - Deserialization failure (if the JSON content cannot be deserialized into a vector of `Embedding`).
///
/// # Examples
///
/// ```no_run
/// let file_path = Path::new("embeddings.json");
/// let embeddings = load_embeddings_from_file(file_path).expect("Failed to load embeddings");
/// println!("{:?}", embeddings);
/// ```
pub fn load_embeddings_from_file(file_path: &Path) -> Result<Vec<Embedding>> {
    // Check if the file exists before attempting to open
    if !file_path.exists() {
        return Err(Error::new(ErrorKind::NotFound, "File not found"));
    }

    // Open the file
    let file = File::open(file_path)?;

    // Memory-map the file for efficient reading
    let mmap = unsafe { MmapOptions::new().map(&file)? };

    // Deserialize the embeddings vector from the memory-mapped file
    let embeddings: Vec<Embedding> = serde_json::from_slice(&mmap)
        .map_err(|e| Error::new(ErrorKind::Other, e.to_string()))?;

    Ok(embeddings)
}
