/// <reference lib="deno.ns" />
import { load } from "jsr:@std/dotenv";

import { 
    credentials, 
    loadPackageDefinition, 
    Client, 
    Channel, 
    ChannelCredentials 
} from "@grpc/grpc-js";

import { loadSync } from "@grpc/proto-loader";
import path from "node:path";
import { readFileSync } from "node:fs";


interface GreeterClient extends Client {
  sayHello(
    request: { name: string },
    callback: (error: any, response: { message: string }) => void
  ): any;
}

async function main() {
    const env = await load();
    const RUST_SERVER = env["RUST_SERVER"];
    console.log(`RUST_SERVER from .env: ${RUST_SERVER}`);
    console.log("STEP 1: Resolving PROTO_PATH..."); // NEW
    const PROTO_PATH = path.resolve("./proto/hello.proto");
    console.log("STEP 2: Loading package definition..."); // NEW
    const packageDefinition = loadSync(PROTO_PATH, {
        keepCase: true,
        longs: String,
        enums: String,
        defaults: true,
        oneofs: true,
    });
    console.log("STEP 3: Package definition loaded."); // NEW

    console.log("STEP 4: Loading helloProto..."); // NEW
    const helloProto: any = loadPackageDefinition(packageDefinition).hello;
    console.log("STEP 5: Creating gRPC client instance..."); // NEW

    const caCert = readFileSync("certifications/ca.pem");
    // const clientKey = readFileSync("certifications/client.key");
    // const clientCert = readFileSync("certifications/client.pem");
    const client = new helloProto.Greeter(
        RUST_SERVER,
        credentials.createSsl(
            caCert
        )
    ) as GreeterClient;

            
    console.log("STEP 6: gRPC client instance created."); // NEW
    const sayHelloPromise = (request: { name: string }): Promise<{ message: string }> => {
        return new Promise((resolve, reject) => {
            client.sayHello(request, (err: any, response: { message: string }) => {
                console.log("Saying helloo");

                if (err) {
                    console.log("Rejecting");
                    return reject(err);
                }

                console.log("Resolving promise");
                resolve(response);
            });
        });
    };

    try {
        console.log("STEP 7: Making gRPC call..."); // NEW
        const response = await sayHelloPromise({ name: "Alice from Deno 🦕" }); // <--- we stuck here
        console.log(response);

        console.log("STEP 8: gRPC call returned successfully."); // NEW
        console.log("Response from Rust server:", response.message);
    } catch (err: any) {
        console.error("STEP 7 FAILED: gRPC Error:", err); // MODIFIED
        if (err.code === status.UNAVAILABLE) {
            console.error("Server is UNAVAILABLE. Make sure the Rust server is running.");
        }
    } finally {
        console.log("STEP 9: Closing client."); // NEW
        client.close();
        console.log("STEP 10: Client closed."); // NEW
    }

    console.log("STEP 11: Calling dummyFunction..."); // NEW
    const dummyFunction: () => Promise<String> = () => {
        return new Promise((res, rej) => {
            return setTimeout(() => {
                return res("Hello, world from dummy!"); // Changed message for clarity
            }, 10000);
        });
    }

    const myMsg: String = await dummyFunction();
    console.log("STEP 12: dummyFunction resolved."); // NEW
    console.log(myMsg);
    console.log("STEP 13: End of main function."); // NEW
}

if (import.meta.main) {
    await main();
}