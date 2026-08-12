import { NextResponse } from "next/server";


export async function  GET() {
    let res = await new Promise((resolve) => {
        setTimeout(() => {
            console.log("Hello, test route!");
            resolve("Hello, world!");
        }, 1000);
    });

    if(!res){
        console.error("Ooops! Our test value failed!");
    }

    return NextResponse.json({"msg": res});
}