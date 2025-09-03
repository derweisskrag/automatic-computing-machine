use jsonwebtoken::{encode, Header, EncodingKey};
use dotenvy::dotenv;
use std::env;
use std::collections::{HashMap, BTreeMap};
use std::io;
use bcrypt::{hash, verify};

// create user model
use serde::{Deserialize, Serialize};

// Store static
fn get_roles() -> Vec<String> {
    vec![
        "admin".to_string(),
        "user".to_string(),
        "guest".to_string(),
    ]
}

// Do we associate actions with roles?
fn get_actions() -> HashMap<String, Vec<String>> {
    let role_actions = vec![
        ("admin", vec!["read".to_string(), "write".to_string(), "delete".to_string()]),
        ("user", vec!["read".to_string(), "write".to_string()]),
        ("guest", vec!["read".to_string()]),
    ];

    let mut role_action_map = HashMap::new();
    for (role, actions) in role_actions {
        role_action_map.insert(role.to_string(), actions);
    }

    role_action_map
}

#[derive(Debug, Serialize, Deserialize)]
struct Role {
    name: String,
    actions: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize)]
struct Action {
    name: String,
    description: String,
}

// Application
#[derive(Debug, Serialize, Deserialize)]
struct App {
    users: Vec<User>,
    roles: Vec<String>,
    actions: HashMap<String, Vec<String>>,
    sessions: BTreeMap<String, String>, // session_id -> user_id
}


#[derive(Serialize, Deserialize)]
struct Claims {
    sub: String, // subject = username
    role: String,
    exp: usize, // expiration
}

#[derive(Debug, Serialize, Deserialize)]
struct User {
    username: String,
    password: String,
    email: String,
    first_name: String,
    last_name: String,
    age: u8,
    is_active: bool,
    is_admin: bool,
    role: String,
}

fn login(username: String, password: String) -> Result<String, String> {
    let users = read_db("db/users.json")?;
    for user in users {
        // Check if the username and password match
        // Huh? That is where Redis comes in handy?
        if user.username == username && verify_password(&user.password, &password).unwrap_or(false) {
            // Generate a JWT token
            let secret = env::var("JWT_SECRET").unwrap_or_else(|_| "default_secret".into());
            let claims = Claims {
                sub: user.username,
                role: user.role, // "user" or "admin"
                exp: (chrono::Utc::now() + chrono::Duration::hours(1)).timestamp() as usize, // 1 hour expiration
            };
            let token = encode(&Header::default(), &claims, &EncodingKey::from_secret(secret.as_ref()))
                .map_err(|_| "Failed to generate token".to_string())?;
            return Ok(token);
        }
    }
    Err("Invalid credentials".to_string())
}

fn register(user: User) -> Result<String, String> {
    // we have to just store the user in a database (json file for simplicity)
    let mut users = read_db("db/users.json")?;
    users.push(user);
    write_db("db/users.json", &users)?;
    Ok("User registered successfully".to_string())
}

fn read_db(path: &str) -> Result<Vec<User>, String> {
    let content = std::fs::read_to_string(path)
        .map_err(|_| "Failed to read the database file".to_string())?;

    let users: Vec<User> = if content.trim().is_empty() {
        Vec::new()
    } else {
        serde_json::from_str(&content)
            .map_err(|_| "Failed to parse JSON into Vec<User>".to_string())?
    };

    Ok(users)
}


fn write_db(path: &str, data: &Vec<User>) -> Result<(), String> {
    let json_data = serde_json::to_string(data)
        .map_err(|_| "Failed to serialize data".to_string())?;
    
    std::fs::write(path, json_data)
        .map_err(|_| "Failed to write to the database file".to_string())
}

// helper function to gather user input
fn ask_user_input_registration() -> Result<User, String> {
    let mut username = String::new();
    let mut password = String::new();
    let mut email = String::new();
    let mut first_name = String::new();
    let mut last_name = String::new();
    let mut age = String::new();
    let mut is_active = "true".to_string(); // Default to true
    let mut is_admin = "false".to_string(); // Default to false
    let mut role = "user".to_string(); // Default role

    println!("Enter username:");
    io::stdin().read_line(&mut username).expect("Failed to read line");
    
    println!("Enter password:");
    io::stdin().read_line(&mut password).expect("Failed to read line");
    
    println!("Enter email:");
    io::stdin().read_line(&mut email).expect("Failed to read line");
    
    println!("Enter first name:");
    io::stdin().read_line(&mut first_name).expect("Failed to read line");
    
    println!("Enter last name:");
    io::stdin().read_line(&mut last_name).expect("Failed to read line");
    
    println!("Enter age:");
    io::stdin().read_line(&mut age).expect("Failed to read line");
    
    // println!("Is active (true/false):");
    // io::stdin().read_line(&mut is_active).expect("Failed to read line");
    
    // println!("Is admin (true/false):");
    // io::stdin().read_line(&mut is_admin).expect("Failed to read line");
    
    // println!("Enter role:");
    // io::stdin().read_line(&mut role).expect("Failed to read line");

    Ok(User {
        username: username.trim().to_string(),
        password: password.trim().to_string(),
        email: email.trim().to_string(),
        first_name: first_name.trim().to_string(),
        last_name: last_name.trim().to_string(),
        age: age.trim().parse::<u8>().unwrap_or(0),
        is_active: is_active.trim() == "true",
        is_admin: is_admin.trim() == "true",
        role: role.trim().to_string(),
    })
}


fn ask_user_input_login() -> Result<(String, String), String> {
    let mut username = String::new();
    let mut password = String::new();

    println!("Enter username:");
    io::stdin().read_line(&mut username).expect("Failed to read line");
    
    println!("Enter password:");
    io::stdin().read_line(&mut password).expect("Failed to read line");

    Ok((username.trim().to_string(), password.trim().to_string()))
}

fn hash_password(password: &str) -> Result<String, String> {
    hash(password, 4).map_err(|_| "Failed to hash password".to_string())
}


fn verify_password(hashed: &str, password: &str) -> Result<bool, String> {
    verify(password, hashed).map_err(|_| "Failed to verify password".to_string())
}


fn get_sessions() -> BTreeMap<String, String> {
    let mut sessions: BTreeMap<String, String> = BTreeMap::new();
    sessions
}


fn set_up_app() -> Result<App, String> {
    // Initialize the database if it doesn't exist
    if !std::path::Path::new("db/users.json").exists() {
        let initial_users: Vec<User> = vec![];
        write_db("db/users.json", &initial_users)?;
    }

    // Load environment variables
    dotenv().ok();

    // initialize roles and sessions
    let roles = get_roles();
    let actions = get_actions();
    let sessions = get_sessions();
    
    Ok(App {
        users: Vec::new(),
        roles,
        actions,
        sessions,
    })
}



fn main() {
    let app = set_up_app().expect("Failed to set up app");
    // println!("App initialized with roles: {:?}", app.roles);
    // println!("App initialized with actions: {:?}", app.actions);
    // println!("App initialized with sessions: {:?}", app.sessions);

    // ask_user_input_registration()
    //     .and_then(|user| {
    //         let hashed_password = hash_password(&user.password)?;
    //         let new_user = User {
    //             password: hashed_password,
    //             ..user
    //         };
    //         register(new_user)
    //     })
    //     .expect("Failed to register user");

    ask_user_input_login()
        .and_then(|(username, password)| {
            login(username, password)
                .map_err(|e| e.to_string())
        })
        .and_then(|token| {
            println!("Login successful! Token: {}", token);
            Ok(())
        })
        .unwrap_or_else(|e| {
            println!("Error: {}", e);
        });
}
    
