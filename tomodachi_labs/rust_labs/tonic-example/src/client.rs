use hello::greeter_client::GreeterClient;
use hello::HelloRequest;

pub mod hello {
    tonic::include_proto!("hello");
}

use tonic::transport::{Channel, ClientTlsConfig, Certificate};
use tokio::fs; // For reading the certificate file

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let ca_cert_pem = fs::read("certifications/server.pem").await?;
    let ca_cert = Certificate::from_pem(ca_cert_pem);

    let tls_config = ClientTlsConfig::new()
        // For a self-signed cert where you're just verifying the server,
        // you provide the server's certificate as the trusted CA.
        .ca_certificate(ca_cert)
        // Set the domain name the client expects. This should match the CN (Common Name)
        // you put in your server's certificate (e.g., "localhost").
        // IMPORTANT: If you used a different CN, update it here.
        .domain_name("localhost"); // <-- Match your server.pem CN


    let channel = Channel::from_static("https://127.0.0.1:50051") // <-- Use https://
        .tls_config(tls_config)? // Apply the TLS configuration
        .connect()
        .await?;

    // 4. Create the GreeterClient with the TLS-enabled channel
    let mut client = GreeterClient::new(channel); // Pass the channel to the client constructor

    let request = tonic::Request::new(HelloRequest {
        name: "Alice from Rust (TLS Client)".into(), // Updated name for clarity
    });

    let response = client.say_hello(request).await?;

    println!("Response from TLS-enabled Rust server: {}", response.into_inner().message);

    Ok(())
}