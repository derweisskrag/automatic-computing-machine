import { NextResponse } from "next/server";
import type { PredictionRequest } from "@/common_types/wind_data";

export async function GET() {
    await new Promise<void>((resolve) => { 
        setTimeout(() => {
            console.log("Hello, async!");
            resolve();
        }, 1000); 
    });

    return new NextResponse<string>("Mock endpoint complete!");
}

function isError(e: unknown): e is Error {
  return e instanceof Error;
}

export async function POST(request: Request) {
  try {
    const rawBody = await request.text();
    console.log("Raw body received:", rawBody);


    const data: PredictionRequest = JSON.parse(rawBody);
    console.log(`Data came to us: ${data}`);

    // Remove Wind_Speed_Squared and Wind_Speed_Cubed if calculated client-side
    // or calculate them here:
    const wind_speed_squared = Math.pow(data.Wind_Speed, 2);
    const wind_speed_cubed = Math.pow(data.Wind_Speed, 3);

    // Prepare payload for Python
    const payload = {
      ...data,
      Wind_Speed_Squared: wind_speed_squared,
      Wind_Speed_Cubed: wind_speed_cubed,
    };

    // Make request to Python API
    const pythonResponse = await fetch(`${process.env.PYTHON_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!pythonResponse.ok) {
      throw new Error(`Python server responded with ${pythonResponse.status}`);
    }

    const result = await pythonResponse.json();

    return NextResponse.json(result);
  } catch (error) {

    console.error("Error in POST handler:", error);

    const message = error instanceof Error
        ? error.message
        : "An unexpected error occurred.";

    return NextResponse.json<{ error: string }>(
        { error: message },
        { status: 500 }
    );

    }
}