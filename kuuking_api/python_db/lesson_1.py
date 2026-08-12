import psycopg2
import asyncpg

def create_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="kuuking",
        port=5432
    )
    return conn

def read_data():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cats")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def create_connection_async():
    
    return asyncpg.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="kuuking",
        port=5432
    )


async def read_data_async():
    conn = await create_connection_async()
    rows = await conn.fetch("SELECT * FROM Cats")
    await conn.close()
    return rows

if __name__ == "__main__":
    # data = read_data()
    # for row in data:
    #     print(row)

    import asyncio
    async def main():
        data = await read_data_async()
        for row in data:
            print(f"{row['name']} is a {row['breed']}, {row['age']} years old.")


    asyncio.run(main())