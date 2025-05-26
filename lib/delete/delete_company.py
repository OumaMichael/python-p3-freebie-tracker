#!/usr/bin/env python3

import sqlite3
import os

def delete_company():
    """Delete company with id=4 and name='Test Company' using SQLite3"""
    
    # Path to database (go up one level to lib folder)
    db_path = os.path.join(os.path.dirname(__file__), '..', 'freebies.db')
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Checking for company with ID=4 and name='Test Company'...")
        
        # Check if company exists
        cursor.execute("SELECT * FROM companies WHERE id = 4 AND name = 'Test Company'")
        company = cursor.fetchone()
        
        if not company:
            print(" Company with ID=4 and name 'Test Company' not found")
            return
        
        print(f" Found company: ID={company[0]}, Name='{company[1]}', Founded={company[2]}")
        
        # Check for related freebies
        cursor.execute("SELECT COUNT(*) FROM freebies WHERE company_id = 4")
        freebie_count = cursor.fetchone()[0]
        
        if freebie_count > 0:
            print(f"  Company has {freebie_count} related freebies. Deleting them first...")
            cursor.execute("DELETE FROM freebies WHERE company_id = 4")
            print(f" Deleted {cursor.rowcount} freebies")
        
        # Delete the company
        cursor.execute("DELETE FROM companies WHERE id = 4 AND name = 'Test Company'")
        
        if cursor.rowcount > 0:
            conn.commit()
            print(" Successfully deleted 'Test Company' with ID=4")
        else:
            print(" No company was deleted")
            
    except sqlite3.Error as e:
        print(f" Database error: {e}")
        conn.rollback()
    except Exception as e:
        print(f" Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    delete_company()