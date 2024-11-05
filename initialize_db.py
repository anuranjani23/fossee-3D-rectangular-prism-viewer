import sqlite3

def setup_test_database():
    """Set up the SQLite database with test cases and standard examples."""
    
    conn = sqlite3.connect('prisms.db')
    cursor = conn.cursor()
    
    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prisms (
            designation TEXT PRIMARY KEY,
            length REAL,
            width REAL,
            height REAL
        )
    ''')
    
    # Test cases from the unit tests plus some standard examples
    prism_data = [
        # Standard examples
        ('STD-001', 40.0, 20.0, 100.0),  # Original example
        ('STD-002', 30.0, 15.0, 80.0),   # Another standard case
        
        # Test cases from unit tests
        ('TEST-001', 10.0, 5.0, 2.0),    # Standard test case
        ('TEST-002', 1.0, 1.0, 1.0),     # Unit cube
        ('TEST-003', 10.0, 10.0, 10.0),  # Equal dimensions
        
        # Additional examples for visualization
        ('LONG-001', 100.0, 10.0, 10.0), # Long prism
        ('TALL-001', 10.0, 10.0, 100.0), # Tall prism
        ('WIDE-001', 10.0, 100.0, 10.0), # Wide prism
        ('CUBE-001', 50.0, 50.0, 50.0),  # Large cube
        ('FLAT-001', 100.0, 100.0, 1.0), # Flat plate
    ]
    
    # Clear existing data
    cursor.execute('DELETE FROM prisms')
    
    # Insert the test cases
    cursor.executemany(
        'INSERT INTO prisms (designation, length, width, height) VALUES (?, ?, ?, ?)',
        prism_data
    )
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database setup completed successfully!")
    print(f"Added {len(prism_data)} prism configurations to the database.")

if __name__ == "__main__":
    setup_test_database()