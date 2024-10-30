import sqlite3

def initialize_database(db_name='prisms.db'):
    """
    Initializes a SQLite database with a table for storing prism data.
    
    Parameters:
        db_name (str): The name of the database file.
    """
    try:
        # Connect to the SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Create the 'prisms' table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prisms (
                designation TEXT PRIMARY KEY,  -- unique identifier for each prism
                length REAL NOT NULL,          -- length of the prism
                width REAL NOT NULL,           -- width of the prism
                height REAL NOT NULL           -- height of the prism
            )
        ''')
        
        # Sample data to be inserted (replace existing if the key matches)
        sample_data = [
            ('PRISM_1', 40.0, 20.0, 100.0),
            ('PRISM_2', 50.0, 30.0, 80.0),
            ('PRISM_3', 60.0, 25.0, 90.0)
        ]
        
        # Insert or replace sample data into the 'prisms' table
        cursor.executemany('INSERT OR REPLACE INTO prisms VALUES (?, ?, ?, ?)', sample_data)
        
        # Commit the transaction to save changes
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        # Ensure the connection is closed after operations
        conn.close()

if __name__ == "__main__":
    initialize_database()
