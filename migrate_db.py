import sqlite3
from datetime import datetime


def migrate_database():
    """Add the year column to the transactions table"""
    print("Starting database migration...")
    
    # Connect to the database
    conn = sqlite3.connect('data/zzp_tracker.db')
    cursor = conn.cursor()
    
    try:
        # Check if the year column already exists
        cursor.execute("PRAGMA table_info(transactions)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'year' not in columns:
            print("Adding 'year' column to transactions table...")
            
            # Add the year column
            cursor.execute("ALTER TABLE transactions ADD COLUMN year INTEGER")
            
            # Update existing records with the year from the date field
            cursor.execute("UPDATE transactions SET year = strftime('%Y', date)")
            
            # Commit the changes
            conn.commit()
            print("Migration completed successfully!")
        else:
            print("The 'year' column already exists in the transactions table.")
    
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    migrate_database() 