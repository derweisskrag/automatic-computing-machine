use auth_rust::{
    login,
    signup,
    RequestAuthSignUp
};

use futures_util::TryStreamExt;
use std::pin::Pin;
use dotenvy::dotenv;
use std::env;

use sqlx::{postgres::PgPoolOptions, FromRow, PgPool};
use sqlx::Row;
use sqlx::types::chrono::NaiveDate;

use axum::{
    routing::{post, get},
    Router,
    response::{IntoResponse, Json},
    body::Body,
    extract::Json as ExtractJson,
    extract::State,
    extract::Query
};


// For complex query params
use sqlx::QueryBuilder; 

use serde_json::{Value, json};
use serde::{Deserialize, Serialize}; 
use tokio::signal;

// adding hash
use bcrypt::{hash, DEFAULT_COST, verify};

// use std::sync::Arc;
// type AppState = Arc<PgPool>;

// Define your application state struct.
// It will hold the database pool and the JWT secret.
#[derive(Clone)] // Derive Clone so it can be safely shared across tasks in Axum
pub struct AppState {
    pub pool: PgPool,
    pub jwt_secret: String,
    // Add other shared resources here as needed
}

// You might also want to add helper methods to AppState if it grows
// For example, to easily access parts of the state.
impl AppState {
    pub fn new(pool: PgPool, jwt_secret: String) -> Self {
        AppState { pool, jwt_secret }
    }
}


// Prepare the simple auth
#[derive(Debug, Deserialize)]
struct AuthRequest {
    password: String,
    email: String
}


// The response for Auth
#[derive(Debug, Serialize)]
struct AuthResponse {
    jwt: String // You're in
}


// Cat
#[derive(Debug, sqlx::FromRow, Serialize)]
pub struct Cat {
    pub id: i32,
    pub name: Option<String>,
    pub breed: Option<String>,
    pub age: Option<i32>,
    pub is_adopted: Option<bool>,
    pub arrival_date: Option<NaiveDate>,
}


#[derive(serde::Deserialize)]
struct CatRequest {
    id: i32,
}


#[derive(Deserialize)]
struct AdoptedFilter {
    adopted: Option<bool>,
}


// Route handler: GET /cats
async fn get_cats(State(app_state): State<AppState>, Query(filter): Query<AdoptedFilter>) -> Result<Json<Vec<Cat>>, (axum::http::StatusCode, String)> {
    let mut builder = QueryBuilder::<sqlx::Postgres>::new("SELECT * FROM cats");

    
    // Potentially using MATCH syntax to
    // None => {} <-- handle None
    if let Some(true) = filter.adopted {
        builder.push(" WHERE is_adopted = true");
    } else if let Some(false) = filter.adopted {
        builder.push(" WHERE is_adopted = false");
    }

    println!("Query: {}", builder.sql());
    // let result = sqlx::query_as::<_, Cat>(query)
    //     .fetch_all(&pool)
    //     .await;

    let result = builder
        .build_query_as::<Cat>() // tells sqlx: map results into Cat
        .fetch_all(&app_state.pool)        // run it
        .await;
    

    match result {
        Ok(cats) => Ok(Json(cats)),
        Err(err) => Err((
            axum::http::StatusCode::INTERNAL_SERVER_ERROR,
            format!("Failed to fetch cats: {}", err),
        )),
    }
}


async fn get_one_cat(State(app_state): State<AppState>, ExtractJson(payload): ExtractJson<CatRequest>) -> Result<Json<Cat>, (axum::http::StatusCode, String)> {
    let result = sqlx::query_as::<_, Cat>("SELECT * FROM Cats WHERE id = $1") // Fetch any kind of cat given the id
        .bind(payload.id)
        .fetch_one(&app_state.pool)
        .await;

    match result {
        Ok(cat) => Ok(Json(cat)),
        Err(err) => Err((
            axum::http::StatusCode::INTERNAL_SERVER_ERROR,
            format!("Unable to find the cat, use your filter dammit!: {}", err),
        )),
    }
}


// we can track signals:
async fn shutdown_signal() {
    signal::ctrl_c()
        .await
        .expect("Failed to install CTRL + C signal handler");

    println!("Server shutting down...");
}


#[tokio::main]
async fn main() -> Result<(), sqlx::Error> {
    dotenv().ok();
    let db_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set");
    println!("Connecting to database at: {}", db_url);

    // get jwt secret and password
    let jwt_secret = env::var("JWT_SECRET").expect("JWT_SECRET must be found");
    let secret_password = env::var("ADMIN_PASSWORD").expect("ADMIN_PASSWORD must exist");
    // let hashed_password = hash(&secret_password, DEFAULT_COST);


    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&db_url)
        .await?;

    
    let token = login("admin".to_string(), secret_password, &pool, &jwt_secret).await;

    match token {
        Ok(token) => println!("We got token: {}", token),
        Err(err) => println!("We got an error: {}", err)
    }

    // Hashing for alice
    let hashed_password = hash("alice_penguin", DEFAULT_COST);

    match hashed_password {
        Ok(ref hashed) => println!("Hash the password for alice (alice_penguin): {}", hashed),
        Err(_) => println!("Could not hash the password")
    }

//         |
//                                           ^^^^^^^^^^^^^^^ value used here after
// partial move
//     |
//     = note: partial move occurs because value has type `std::string::String`, wh
// ich does not implement the `Copy` trait
// help: borrow this binding in the pattern to avoid moving the value
//     |
// 186 |         Ok(ref hashed) => println!("Hash the password for alice (alice_pen
// guin): {}", hashed),


    match signup(RequestAuthSignUp { username: "Alice".to_string(), email: "Alice@gmail.com".to_string(), password_hash: hashed_password.expect("REASON") }, &pool, &jwt_secret).await {
        Ok(_) => println!("Alice was created successfully!"),
        Err(err) => println!("We failed to create Alice due to {}", err)
    }


    // Log the connection
    println!("Connected to ElephantSQL");


    // Create an instance of our custom AppState
    // let app_state = AppState::new(pool.clone(), jwt_secret);


    // // Build our application with multiple routes
    // // I applied filter to my route (/cats?adopted=true)
    // // Removed: QUERY from /get_one_cat
    // // Insight: Axum allows to use State, Query, JSON order.
    // let app = Router::new()
    //     .route("/", get(|| async { "Hello from Axum!" }))
    //     .route("/cats", get(get_cats as fn(State<AppState>, Query<AdoptedFilter>) -> _))
    //     .route("/get_one_cat", post(get_one_cat as fn(State<AppState>, ExtractJson<CatRequest>) -> _))
    //     .with_state(app_state); 


    // // Run our app with hyper, listening globally on port 3010
    // let listener = tokio::net::TcpListener::bind("0.0.0.0:3010").await.unwrap();

    // println!("Serving on 3010 port...");

    // // try to use tokio::signal
    // axum::serve(listener, app)
    //     .with_graceful_shutdown(shutdown_signal())
    //     .await
    //     .unwrap();

    Ok(())
}
