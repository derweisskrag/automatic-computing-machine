use axum::{
    routing::{post, get},
    Router,
    response::{IntoResponse, Json},
    body::Body,
    extract::Json as ExtractJson
};

// if you want to use .env
use dotenvy::dotenv;

// For handling data & signals
use serde_json::{Value, json};
use serde::{Deserialize, Serialize}; 
use tokio::signal;

// Using Serde we can serialize and deserialize:
#[derive(Debug, Deserialize)]
struct GreetRequest {
    name: String,
}

#[derive(Debug, Serialize)]
struct GreetResponse {
    message: String,
}


// POST: Greet a person given their name
async fn greet(ExtractJson(payload): ExtractJson<GreetRequest>) -> Json<GreetResponse> {
    let message = format!("Hello, {}!", payload.name);
    Json(GreetResponse { message })
}


// GET: Shows the greetings!
async fn hello() -> impl IntoResponse {
    "Greetings, guest!"
}


// Plain Text:
// `&'static str` becomes a `200 OK` with `content-type: text/plain; charset=utf-8`
async fn plain_text() -> &'static str {
    "foo"
}


// JSON:
// `Json` gives a content-type of `application/json` and works with any type
// that implements `serde::Serialize`
async fn json() -> Json<Value> {
    Json(json!({ "data": 42 }))
}


// we can track signals:
async fn shutdown_signal() {
    signal::ctrl_c()
        .await
        .expect("Failed to install CTRL + C signal handler");

    println!("Server shutting down...");
}


#[tokio::main]
async fn main() {
    // Build our application with multiple routes
    let app = Router::new()
        .route("/", get(|| async { "Home route" }))
        .route("/hello", get(hello))
        .route("/plain_text", get(plain_text))
        .route("/json", get(json))
        .route("/greet", post(greet));


    // Run our app with hyper, listening globally on port 3010
    let listener = tokio::net::TcpListener::bind("0.0.0.0:3010").await.unwrap();

    println!("Serving on 3010 port...");

    // try to use tokio::signal
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await
        .unwrap();
}
