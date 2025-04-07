import sqlite3
from datetime import datetime


def sample_migration_add_year_field():
    """Add the year column to the transactions table"""
    print("Starting database migration...")
    
    # Connect to the database
    conn = sqlite3.connect('data/zzp_tracker.db')
    cursor = conn.cursor()
    
    try:
        # Check if the year column already exists
        cursor.execute("PRAGMA table_info(transactions)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'year' in columns:
            print("Setting 'year' column to NOT NULL in transactions table...")
            
            # SQLite doesn't support ALTER COLUMN directly
            # We need to create a new table, copy the data, drop the old table, and rename the new one
            cursor.execute("""
                CREATE TABLE transactions_new (
                    id INTEGER PRIMARY KEY,
                    date TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    counterparty TEXT NOT NULL,
                    net_amount NUMERIC(10, 2) NOT NULL,
                    vat_amount NUMERIC(10, 2) NOT NULL,
                    gross_amount NUMERIC(10, 2) NOT NULL,
                    type TEXT NOT NULL,
                    category TEXT NOT NULL,
                    status TEXT NOT NULL
                )
            """)
            
            # Copy data from the old table to the new table
            cursor.execute("""
                INSERT INTO transactions_new 
                SELECT id, date, year, description, counterparty, net_amount, vat_amount, 
                       gross_amount, type, category, status 
                FROM transactions
            """)
            
            # Drop the old table
            cursor.execute("DROP TABLE transactions")
            
            # Rename the new table to the original name
            cursor.execute("ALTER TABLE transactions_new RENAME TO transactions")
            
            # Commit the changes
            conn.commit()
            print("Migration completed successfully!")
        else:
            print("The 'year' column does not exist in the transactions table.")
    
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    sample_migration_add_year_field()