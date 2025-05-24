#!/usr/bin/env python3

import sqlite3
import os

def connect_to_db():
    """Create connection to the SQLite database in lib folder"""
    try:
        # Get path to lib folder where freebies.db is located
        db_path = os.path.join(os.path.dirname(__file__), '..', 'freebies.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def essential_joins():
    """Demonstrate the 4 most important SQL join patterns"""
    conn = connect_to_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    print("ESSENTIAL SQL JOIN PATTERNS")
    print("=" * 50)
    
    try:
        # 1. INNER JOIN - Most common join
        print("\n1. INNER JOIN:")
        print("Shows freebies with dev and company names")
        print("-" * 40)
        
        query = """
        SELECT 
            f.item_name,
            f.value,
            d.name as dev_name,
            c.name as company_name
        FROM freebies f
        INNER JOIN devs d ON f.dev_id = d.id
        INNER JOIN companies c ON f.company_id = c.id
        ORDER BY f.value DESC
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        for row in results:
            print(f"{row['dev_name']} got {row['item_name']} (KSh {row['value']:,}) from {row['company_name']}")
        
        # 2. LEFT JOIN - Include all records from left table
        print("\n\n2. LEFT JOIN:")
        print("Shows all devs, even those without freebies")
        print("-" * 40)
        
        query = """
        SELECT 
            d.name as dev_name,
            COUNT(f.id) as freebie_count,
            COALESCE(SUM(f.value), 0) as total_value
        FROM devs d
        LEFT JOIN freebies f ON d.id = f.dev_id
        GROUP BY d.id, d.name
        ORDER BY total_value DESC
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        for row in results:
            print(f"{row['dev_name']}: {row['freebie_count']} freebies, Total: KSh {row['total_value']:,}")
        
        # 3. GROUP BY with JOIN - Aggregation across tables
        print("\n\n3. GROUP BY with JOIN:")
        print("Company performance summary")
        print("-" * 40)
        
        query = """
        SELECT 
            c.name as company_name,
            COUNT(f.id) as freebies_given,
            COALESCE(SUM(f.value), 0) as total_spent,
            COUNT(DISTINCT f.dev_id) as devs_reached
        FROM companies c
        LEFT JOIN freebies f ON c.id = f.company_id
        GROUP BY c.id, c.name
        ORDER BY total_spent DESC
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        for row in results:
            print(f"{row['company_name']}: {row['freebies_given']} freebies, KSh {row['total_spent']:,}, {row['devs_reached']} devs")
        
        # 4. WHERE with JOIN - Filtered joins
        print("\n\n4. WHERE with JOIN:")
        print("High-value freebies (> KSh 1M)")
        print("-" * 40)
        
        query = """
        SELECT 
            d.name as dev_name,
            f.item_name,
            f.value,
            c.name as company_name
        FROM freebies f
        INNER JOIN devs d ON f.dev_id = d.id
        INNER JOIN companies c ON f.company_id = c.id
        WHERE f.value > 1000000
        ORDER BY f.value DESC
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            for row in results:
                print(f"{row['dev_name']} got {row['item_name']} (KSh {row['value']:,}) from {row['company_name']}")
        else:
            print("No high-value freebies found")
        
    except sqlite3.Error as e:
        print(f"Error executing queries: {e}")
    
    finally:
        conn.close()

def quick_stats():
    """Show quick database statistics"""
    conn = connect_to_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    print("\n\nQUICK DATABASE STATS")
    print("=" * 30)
    
    try:
        # Count records
        cursor.execute("SELECT COUNT(*) FROM companies")
        companies = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM devs")
        devs = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM freebies")
        freebies = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(value) FROM freebies")
        total_value = cursor.fetchone()[0] or 0
        
        print(f"Companies: {companies}")
        print(f"Developers: {devs}")
        print(f"Freebies: {freebies}")
        print(f"Total Value: KSh {total_value:,}")
        
    except sqlite3.Error as e:
        print(f"Error getting stats: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    quick_stats()
    essential_joins()