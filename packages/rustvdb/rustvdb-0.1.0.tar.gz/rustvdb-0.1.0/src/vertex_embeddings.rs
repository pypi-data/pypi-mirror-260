//vertex_embeddings.rs

use google_cloud_auth::project::{Config, create_token_source};
use reqwest::Client;
use serde::{Deserialize, Serialize};
use tokio::time::{interval, Duration};
use anyhow::{Result, Context, anyhow};
use std::{cell::RefCell, time::Instant};
use log::{info, debug};

/// Represents a cached token and its expiry time.
struct CachedToken {
    token: Option<String>, // Now optional, as it might not be immediately available
    expiry: Instant,
}

// Use thread_local storage for caching the token and project details
thread_local! {
    static TOKEN_CACHE: RefCell<Option<CachedToken>> = RefCell::new(None);
    static PROJECT_ID: RefCell<String> = RefCell::new(String::new());
    static LOCATION: RefCell<String> = RefCell::new(String::new());
    static QPS: RefCell<u64> = RefCell::new(1);
}

#[derive(Serialize)]
struct RequestBody<'a> {
    instances: Vec<Instance<'a>>,
}

#[derive(Serialize)]
struct Instance<'a> {
    task_type: &'a str,
    title: &'a str,
    content: &'a str,
}

#[derive(Deserialize, Debug)]
pub struct ResponseBody {
    predictions: Vec<Prediction>,
}

#[derive(Deserialize, Debug)]
pub struct Prediction {
    embeddings: Embedding,
}

#[derive(Deserialize, Debug)]
pub struct Embedding {
    statistics: Statistics,
    values: Vec<f32>,
}

#[derive(Deserialize, Debug)]
pub struct Statistics {
    truncated: bool,
    token_count: i32,
}

/// Initializes the module with project details and QPS settings.
///
/// # Arguments:
///
/// * `project_id`: Google Cloud project ID.
/// * `location`: Google Cloud region.
/// * `qps`: Maximum number of requests per second.
pub fn v_init(project_id: &str, location: &str, qps: u64) -> Result<()> {
    PROJECT_ID.with(|p| *p.borrow_mut() = project_id.to_string());
    LOCATION.with(|l| *l.borrow_mut() = location.to_string());
    QPS.with(|q| *q.borrow_mut() = qps);
    Ok(())
}

/// Gets a valid token, either from the cache or by requesting a new one.
///
/// # Arguments:
///
/// * `config`: Google Cloud authentication configuration.
async fn get_or_refresh_token(config: &Config<'_>) -> Result<String, anyhow::Error> {
    let mut token_to_return = None;
    let mut needs_refresh = false;

    // Check if a new token is needed without performing async operations
    TOKEN_CACHE.with(|cached| {
        let cached = cached.borrow();
        if let Some(cached_token) = &*cached {
            if Instant::now() < cached_token.expiry {
                if let Some(token) = &cached_token.token {
                    token_to_return = Some(token.clone());
                }
            } else {
                needs_refresh = true;
            }
        } else {
            needs_refresh = true;
        }
    });

    // Return the cached token if valid
    if let Some(token) = token_to_return {
        debug!("Reusing cached token.");
        return Ok(token);
    }

    // Refresh the token if needed
    if needs_refresh {
        debug!("Token expired or not set, acquiring new token.");
        let ts = create_token_source(config.clone()).await.context("Failed to create token source")?;
        let token = ts.token().await.context("Failed to get token")?;
        debug!("Token acquired successfully.");

        // Assuming an expiry time of 60 minutes for the token; adjust as needed
        let expiry = Instant::now() + Duration::from_secs(60 * 60);

        // Update the cache with the new token
        TOKEN_CACHE.with(|cached| {
            *cached.borrow_mut() = Some(CachedToken {
                token: Some(token.access_token.clone()),
                expiry,
            });
        });

        return Ok(token.access_token);
    }

    Err(anyhow!("Failed to acquire token"))
}

/// Fetches embeddings from the Google Cloud AI Platform.
///
/// # Arguments:
///
/// * `title`: Title of the document.
/// * `content`: Content of the document.
/// * `mode_str`: Ignored - not used in the current logic.
pub async fn fetch_embeddings(title: &str, content: &str, mode_str: &str) -> Result<Vec<f32>> {
    // Get project details and QPS from thread-local storage
    let project_id = PROJECT_ID.with(|p| p.borrow().clone());
    let location = LOCATION.with(|l| l.borrow().clone());
    let qps = QPS.with(|q| q.borrow().clone());

    // Configuration for Google Cloud authentication
    let config = Config {
        audience: Some("https://aiplatform.googleapis.com/"),
        scopes: Some(&["https://www.googleapis.com/auth/cloud-platform"]),
        ..Default::default()
    };

    // Obtain a valid token
    let token_string = get_or_refresh_token(&config).await.context("Failed to obtain token")?;

    // Model ID and URL for the API request
    let model_id = "textembedding-gecko@003";
    let url = format!(
        "https://us-central1-aiplatform.googleapis.com/v1/projects/{}/locations/{}/publishers/google/models/{}:predict",
        project_id, location, model_id
    );

    // Initialize HTTP client and calculate interval to respect QPS limit
    let client = Client::new();
    let interval_ms = 1000 / qps.max(1); // Ensure qps is at least 1 to avoid division by zero
    let mut interval = interval(Duration::from_millis(interval_ms));

    // Log QPS settings
    debug!("QPS: {}", qps);
    debug!("Interval milliseconds: {}", interval_ms);

    // Wait for initial interval tick to enforce QPS from the start
    interval.tick().await;

    // Construct request body with provided title and content
    let body = RequestBody {
        instances: vec![Instance {
            task_type: "RETRIEVAL_DOCUMENT",
            title,
            content,
        }],
    };

    // Send request with bearer token for authentication
    let res = client.post(&url)
        .bearer_auth(token_string)
        .json(&body)
        .send()
        .await.context("Failed to send request")?;

    // Wait for next interval tick to respect QPS limit
    let start_time = Instant::now();
    interval.tick().await;
    let elapsed_time = start_time.elapsed();
    debug!("Request interval: {:?}", elapsed_time);

    // Extract embeddings from response
    match res.json::<ResponseBody>().await {
        Ok(response_body) => {
            if let Some(prediction) = response_body.predictions.first() {
                Ok(prediction.embeddings.values.clone())
            } else {
                Err(anyhow!("No predictions found"))
            }
        },
        Err(e) => Err(anyhow!(e)).context("Failed to parse response body")
    }
}