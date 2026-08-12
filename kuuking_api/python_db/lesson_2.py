import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = sqlite3.connect(db_file)
    return conn

def read_data(conn):
    """Query all rows in the Cats table."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cats")
    rows = cursor.fetchall()
    cursor.close()
    return rows


