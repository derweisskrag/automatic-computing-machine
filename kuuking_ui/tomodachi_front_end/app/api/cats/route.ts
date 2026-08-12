/*
This API endpoint reads the PostgreSQL database to fetch cat data.

*/

// import NextReponse & PrismaClient
import { NextResponse } from 'next/server';
import { PrismaClient } from '@/app/generated/prisma';
import { z } from 'zod';
import { CatSchema } from "@/lib/schemas/cat.schema"; // Import the schema!
import type { Cat } from "@/lib/schemas/cat.schema"; // Import the type for type safety


const prisma = new PrismaClient();



export async function GET() {
    try {
        const rawCats = await prisma.cats.findMany();
        const cats: Cat[] = rawCats.map(cat => ({
            ...cat,
            name: cat.name ?? "Unknown",
            breed: cat.breed ?? "Unknown",
            age: cat.age ?? 0,
            is_adopted: cat.is_adopted ?? false,
            arrival_date: cat.arrival_date?.toISOString() ?? new Date().toISOString(),
            }));
        
        return NextResponse.json(cats);
    } catch (error: any) {
        console.error('Error fetching cats:', error?.message ?? error);
        return NextResponse.json(
            { error: error?.message ?? 'Unknown error' },
            { status: 500 }
        );
    }
}


export async function POST(req: Request) {
    const body = await req.json();
    // Validate the body
    const parseResult = CatSchema.safeParse(body);

    if (!parseResult.success) {
        // Return detailed Zod validation error messages
        return NextResponse.json(
        {
            error: 'Invalid input',
            details: parseResult.error.format(),  // detailed field errors here
        },
        { status: 400 }
        );
    }

    // Use the validated data (parseResult.data)
    try {
        const newCat = await prisma.cats.create({
            data: {
            ...parseResult.data,
            arrival_date: parseResult.data.arrival_date
                ? new Date(parseResult.data.arrival_date)
                : new Date(), // fallback to current date if not provided
            },
        });
        return NextResponse.json(newCat);
    } catch (error) {
        console.error('Error adding cat:', error);
        return NextResponse.json({ error: 'Failed to add cat' }, { status: 500 });
    }
}


