/// <reference lib="deno.ns" />


async function main(){
    const conn = await Deno.connectTls({
        hostname: "localhost",
        port: 50051,
        certFile: "./certifications/server.pem",
    });

    console.log(conn);
}


if (import.meta.main) {
  await main();
}