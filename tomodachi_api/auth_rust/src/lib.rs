use sqlx::{postgres::PgPoolOptions, FromRow, PgPool};
use sqlx::Row;
use sqlx::types::chrono::{DateTime, Utc};
use sqlx::QueryBuilder; 
use serde_json::{Value, json};
use serde::{Deserialize, Serialize}; 
use bcrypt::{hash, DEFAULT_COST, verify};
use jsonwebtoken::{encode, Header, EncodingKey};


// pub mod Authorization {

    // Both signup, login use reading .env, i might do the same as with pool: pass it like A PROPS IN REACT?

    // An example of classic auth
    // Added the 3rd parameter: borrowing of pool as in higher level: we got our "with_state(pool.clone())" 
    // in axum serving
    // Missing the type for Token tho!
    // TODO: I can just use RequestAuthLogin, but i still forced to take pool if i wanna query db
    // React be like: my child must have PROPS!!
    pub async fn login(username: String, password_hash: String, pool: &PgPool, jwt_secret: &str) -> Result<String, sqlx::error> {
        let mut builder = QueryBuilder::<sqlx::Postgres>::new("SELECT * FROM users WHERE ");
        builder.push("username = "); // Add the column name and operator as a string
        builder.push_bind(&username); // Add the placeholder and bind the value

        // For debug:
        // println!("Query: {}", builder.sql());

        // Now we can build the query and get the user
        // Can be refactored into UserRepository or we can add trait
        // I can take on pool too? (borrow)
        // Because in Axum we can State(pool) so we have it
        let result = builder
            .build_query_as::<User>() 
            .fetch_one(pool)        
            .await;
        

        match result {
            Ok(user) => {
                // proceed with auth
                // we can use our bcrypt now, as this thing is already hashed, and our thing is also hash
                // CHECK: Tomodachi_labs/rust_labs/jwt-trial
                // verify_password(&user.password, &password).unwrap_or(false)
                // 
                println!("DB: {} | As a param: {}", user.username, username);
                println!("Verification of password: {}", verify(&password_hash, &user.password_hash).unwrap_or(false));

                if username == user.username && verify(&password_hash, &user.password_hash).unwrap_or(false) {
                    // we got to the juicy!
                    // They are authorized
                    // We can do whatever we want.
                    // For example: we can check if they got a token.
                    // To search a token, we must do another db query
                    // Once again: we have to pass a parameter

                    // But what if the token is dead? Maybe his time is still stored, so we have simply issue new one?
                    // So, we fetch it

                    // let refresh_token = sqlx::query_as!(Token, "SELECT * FROM tokens WHERE user_id = $1", user.id)
                    //     .fetch_one(pool)
                    //     .await?;

                    // then we check here:
                    // THIS IS CLIENT SIDE REASONING. MY RUST DOES NOT CARE ABOUT ACCESS TOKEN. HE ONLY ISSUES IT UPON LOGIN.
                    // Case 1: Access token is living and is vald:
                    //      In this situation, we simply return the token. 
                    //      Axum then uses this token to return as JSON (Header: "Bearer TOKEN" format) to the client.
                    //      Client will then use to store it Cookies. 
                    // Case 2: Access token is present and died. 
                    //      My guess is that i can re-use refresh token and issue new access token 
                    //      My access token is not stored in the database
                    // Case 3: Access token is never stored (cookies miss it)
                    //      Issue new one and store as long as refresh token exists

                    let claims = Claims {
                        sub: user.username,
                        role: user.role, // "user" or "admin" // in this situation all users get user
                        exp: (chrono::Utc::now() + chrono::Duration::hours(1)).timestamp() as usize, // 1 hour expiration
                    };

                    let token = encode(&Header::default(), &claims, &EncodingKey::from_secret(jwt_secret.as_ref()))
                        .map_err(|_| "Failed to generate token".to_string())?;
                    
                    // and return it
                    // Now Axum will call our function, pass params, and then he gets token
                    Ok(token)
                } else {
                    Err("Could not authorize due to invalid credentials".to_string())
                }
            },
            Err(err) => Err(
                format!("Failed to find the user: {}", err),
            ),
        }
    }


    // I can use  my type for singup
    // We need:
    //  a) username
    //  b) email
    //  c) password to hash, but usually i wanna already hash the password.
    //     Which means I have hash vs hash in "verify" already. So, I don't use plain password at this layer 
    pub async fn signup(data: RequestAuthSignUp, pool: &PgPool, jwt_secret: &str) -> Result<(), sqlx::error> {
        // It is a new user. She or He has never (I can skip gender - users are anonymous!)
        // So, we simply create them

        // Actually we must check one thing:
        // if let Some() <-- if our data input is wrong then we cannot signup.

        // This query will add new user to the database
        sqlx::query!(
            "INSERT INTO users (username, email, role, password_hash) 
            VALUES ($1, $2, $3, $4)",
            data.username,
            data.email, 
            "user",
            data.password_hash
        )
        .execute(pool)
        .await;

        // So as long as we created the user successfully
        // Now we can query this little cutie
        // Yeah, i probably have to handle this repetetive code (UserRepository might be a good idea or Trait)
        // Issue: does my borrow or creates new?
        // E. g., let username = &data.username or even CLONE it so now after it went to DB call, we can re-use it
        // Or Rust will find it for me? Notice: &pool, so i might actually take here &username too! 
        let user = sqlx::query_as!(User, "SELECT * FROM users WHERE username = $1", data.username)
            .fetch_one(pool)
            .await;

        // If this line is achieved and no Err(T) triggered:
        // Else: Borrowing issue, so we can stick to SQLX pattern (and use & for that username)
        println!("[AUTH]: User with the username {} has been created!", data.username);

        // Then we have to issue them a REFRESH token
        // What kind of this token? Turns out this bad boy is refresh token
        // I might try to set it to 30 days
        // Issue: Will it be DatimeTime<Utc>? I think it should be
        
        let expires_at_datetime: chrono::DateTime<chrono::Utc> = Utc::now() + chrono::Duration::days(30);
        let exp_claim_timestamp = expires_at_datetime.timestamp() as usize;

        let claims = Claims {
            sub: data.username,
            role: "user".to_string(),
            exp: exp_claim_timestamp,
        };

        // Create that token
        let refresh_token = encode(&Header::default(), &claims, &EncodingKey::from_secret(jwt_secret.as_ref()))
            .map_err(|_| "Failed to generate token".to_string())?;

        // After our token is created, we must execute another query
        // What our fields are:
        //     id SERIAL PRIMARY KEY,
        // access_token TEXT NOT NULL,
        // refresh_token TEXT NOT NULL,
        // created_at TIMESTAMPTZ DEFAULT now(), <---- THIS MEANS: Option<DateTime<Utc>>
        // expires_at TIMESTAMPTZ NOT NULL,
        // user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE

        // This information tells us:
        //      a) I have to use my 'refresh_token' variable as TEXT for Postgres
        //      b) expires_at (destruct claims!) - Again: DateTime<Utc> type, Not Option<DateTime<Utc>>
        //      c) ID for the user and this is the hard part. 
        //         We can fetch our user, and then use his id. 
        //         This is because in our db, right now, we can
        //         have thousands of users, and simply putting id from here is wrong
        //         Once I fetched the user from DB, i can pass their id
        // NB! User is fetched at this point!
        sqlx::query!(
            "INSERT INTO tokens (refresh_token, expires_at, user_id) 
            VALUES ($1, $2, $3)",
            refresh_token,
            expires_at_datetime,
            user.unwrap().id 
        )
        .execute(pool)
        .await;

        // We can either fetch token or do whatever we want
        // Result: Database gets the Token table populated with the newly created token. 
        // It knows which user must get it as it fetched the newly created user.
        // Bottleneck? We got 5 connections per pool. We don't use CACHE or REDIS here
        // This means that once i pushed new user to the database, I might get some traffic 
        // on server as I fetching the same exact user from the database.
        Ok(())
    }


    //pub mod Schema {
        #[derive(Debug, sqlx::FromRow, Serialize)]
        pub struct User {
            pub id: i32,
            pub username: String,
            pub email: String,
            pub created_at: Option<DateTime<Utc>>,
            pub role: String,
            pub password_hash: String
        }

        #[derive(Debug, sqlx::FromRow, Serialize, Deserialize)]
        pub struct Token {
            pub id: i32,
            pub refresh_token: String,
            pub created_at: Option<DateTime<Utc>>,
            pub expires_at: DateTime<Utc>,
            pub user_id: i32
        }

        #[derive(Serialize, Deserialize)]
        pub struct Claims {
            sub: String, // subject = username
            role: String,
            exp: usize, // expiration
        }
    //}

    //pub mod RequestAuthData {
        // we only need:
        // username, email, password
        // role = user or guest (but normally, they are always guest)
        #[derive(Debug, Serialize, Deserialize)]
        pub struct RequestAuthSignUp {
            pub username: String,
            pub email: String,
            pub password_hash: String
        }

        // We take on hash to compare hashes
        #[derive(Debug, Serialize, Deserialize)]
        pub struct RequestAuthLogin {
            pub username: String,
            pub password_hash: String
        }
    //}
//}