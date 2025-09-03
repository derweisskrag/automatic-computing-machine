use tonic::{
    transport::Server,
    Request,
    Response,
    Status
};

use tokio::signal;


use std::net::TcpListener;
use tokio_stream::wrappers::TcpListenerStream;
use tonic::transport::ServerTlsConfig;

// let us import 
use tonic::transport::{Identity, Channel, ClientTlsConfig};

pub mod hello {
    tonic::include_proto!("hello"); // proto package name
}

use hello::greeter_server::{Greeter, GreeterServer};
use hello::{HelloReply, HelloRequest};
use tokio::fs; // For reading the certificate file

#[derive(Default)]
pub struct MyGreeter {}

#[tonic::async_trait]
impl Greeter for MyGreeter {
    async fn say_hello(
        &self,
        request: Request<HelloRequest>,
    ) -> Result<Response<HelloReply>, Status> {
        println!("\n[Rust Server] Received SayHello request.");
        let name = request.into_inner().name;
        println!("[Rust Server] Client name: '{}'", name);
        let reply = HelloReply {
            message: format!("Hello, {}!", name),
        };
        println!("[Rust Server] Sending response: '{}'", reply.message);
        Ok(Response::new(reply))
    }
}


#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Bind manually to "localhost:50051" <-- match certificate
    //let std_listener = TcpListener::bind("localhost:50051")?;
    // let incoming = TcpListenerStream::new(tokio::net::TcpListener::from_std(std_listener)?);

    // before:
    let addr = "127.0.0.1:50051".parse().unwrap();



    println!("Server is listening on localhost:50051");

    // Load TLS identity
    let cert = tokio::fs::read("certifications/server.pem").await?;
    let key = tokio::fs::read("certifications/server.key").await?;
    let identity = Identity::from_pem(cert, key);

    let greeter = MyGreeter::default();

    // Start server with TLS and graceful shutdown
    // Server::builder()
    //     .tls_config(ServerTlsConfig::new().identity(identity))?
    //     .add_service(GreeterServer::new(greeter))
    //     .serve_with_incoming_shutdown(incoming, async {
    //         tokio::signal::ctrl_c().await.expect("Failed to listen for Ctrl+C");
    //         println!("Ctrl+C received, shutting down gracefully...");
    //     })
    //     .await?;

    Server::builder()
        .tls_config(ServerTlsConfig::new().identity(identity))?
        .add_service(GreeterServer::new(greeter))
        .serve_with_shutdown(addr, async {
            signal::ctrl_c()
                .await
                .expect("Failed to listen for Ctrl+C");
            println!("Ctrl+C received, shutting down gracefully...");
        })
        .await?;

    Ok(())
}
