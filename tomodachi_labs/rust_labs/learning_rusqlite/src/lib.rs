use rusqlite::{params, Connection, Result};
use serde::Serialize;
use std::ffi::{CStr, CString, c_char};
use std::ptr;



#[derive(Debug, Serialize)]
pub struct Person {
    pub id: i32,
    pub name: String,
}

// Function to connect and create a database connection
#[no_mangle]
pub extern "C" fn create_person_database() -> Result<()> {
    let db_path = "person_data.db";
    let conn = Connection::open(db_path)?;

    conn.execute(
        "CREATE TABLE IF NOT EXISTS person (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            data BLOB
        )",
        [],
    )?;

    Ok(())
}

#[no_mangle]
pub extern "C" fn free_string(ptr: *mut i8) {
    if ptr.is_null() { return; }
    unsafe { let _ = CString::from_raw(ptr); };  // Automatically cleaned up by Rust's ownership semantics
}

// TODO: Check this function out

#[no_mangle]
pub extern "C" fn run_script(sql_query: &str) -> Result<()> {
    let conn = Connection::open("person_data.db");
    conn?.execute(sql_query, [])?;
    Ok(())
}

#[no_mangle]
pub extern "C" fn read_user_db_query() -> *mut i8 {
    let conn = match Connection::open("person_data.db") {
        Ok(conn) => conn,
        Err(_) => return ptr::null_mut(),
    };

    let mut stmt = match conn.prepare("SELECT id, name FROM person") {
        Ok(stmt) => stmt,
        Err(_) => return ptr::null_mut(),
    };

    let person_iter = match stmt.query_map([], |row| {
        let id: i32 = row.get(0)?;
        let name: String = row.get(1)?;
        Ok(Person { id, name })
    }) {
        Ok(iter) => iter,
        Err(_) => return ptr::null_mut(),
    };

    let mut people = Vec::new();
    for person in person_iter {
        match person {
            Ok(p) => people.push(p),
            Err(_) => return ptr::null_mut(),
        }
    }

    let json_string = match serde_json::to_string(&people) {
        Ok(json) => json,
        Err(_) => return ptr::null_mut(),
    };

    let output = CString::new(json_string).expect("CString conversion failed");

    output.into_raw()  // Return a raw pointer to the C-compatible string
}


// Function to insert a person into the database
#[no_mangle]
pub extern "C" fn insert_person(id: i32, name: *const u8) {
    unsafe {
        // Convert the C string pointer to a Rust string slice
        let c_str = if name.is_null() {
            CStr::from_ptr(ptr::null())
        } else {
            std::ffi::CStr::from_ptr(name as *const i8)
        };

        let str_name = match c_str.to_str() {
            Ok(name) => name,
            Err(_) => {
                println!("Failed to convert name to a valid UTF-8 string.");
                return;
            }
        };

        println!("Inserting Person ID: {}, Name: {}", id, str_name);

        match Connection::open("person_data.db") {
            Ok(conn) => {
                let insert_query = "INSERT INTO person (id, name) VALUES (?1, ?2)";
                match conn.execute(insert_query, rusqlite::params![id, str_name]) {
                    Ok(_) => println!("Inserted person into the database."),
                    Err(e) => eprintln!("Database insertion failed: {:?}", e),
                }
            }
            Err(e) => {
                eprintln!("Failed to open the database: {:?}", e);
            }
        }
    }
}


#[no_mangle]
pub extern "C" fn create_db(path: *const c_char, sql_query: *const c_char) -> i32 {
    if path.is_null() || sql_query.is_null() {
        return 1; // Indicate error: null pointer
    }

    unsafe {
        // Convert C strings to Rust strings
        let path = match CStr::from_ptr(path).to_str() {
            Ok(p) => p,
            Err(_) => return 2, // Indicate error: invalid UTF-8
        };

        let sql_query = match CStr::from_ptr(sql_query).to_str() {
            Ok(q) => q,
            Err(_) => return 2,
        };

        // Open the database and execute the query
        match Connection::open(path) {
            Ok(conn) => {
                if let Err(_) = conn.execute(sql_query, []) {
                    return 3; // Indicate error: SQL execution failed
                }
            }
            Err(_) => return 4, // Indicate error: database open failed
        }
    }

    0 // Indicate success
}



// Use the two functions
// Functions above are DB related, but this approach is not Good! I will only test the working functions.
// NEVER CODE LIKE THAT! UNSAFE RUST IS BAD!!! USE ZIG OR C++ DIRECTLY. 
// THESE TWO FUNCTIONS ARE OKAY TO ME

pub fn is_valid(x: i32) -> bool {
    x >= 1 && x <= 4
}


#[no_mangle]
pub extern "C" fn check_result(x: i32, y: i32, z: i32) -> bool {
    if is_valid(x) && is_valid(y) && is_valid(z) {
        return true;
    }

    false
}

#[no_mangle]
pub extern  "C" fn hello_from_rust(){
    println!("Test: Rust worked!");
}

#[no_mangle]
pub const extern "C" fn calculate_new_currency(amount: f32, to_rate: f32, from_rate: f32) -> f32 {
   amount * (to_rate / from_rate)
}

