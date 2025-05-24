#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie

def test_relationships_and_methods():
    """Test all the relationships and methods with the seed data"""
    
    # Create engine and session
    engine = create_engine('sqlite:///lib/freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("=" * 60)
    print("TESTING SQLALCHEMY RELATIONSHIPS AND METHODS")
    print("=" * 60)
    
    # Get test data
    raila = session.query(Dev).filter_by(name="Raila").first()
    ruto = session.query(Dev).filter_by(name="Ruto").first()
    rigachi = session.query(Dev).filter_by(name="Rigachi").first()
    
    odm = session.query(Company).filter_by(name="ODM").first()
    uda = session.query(Company).filter_by(name="UDA").first()
    dcp = session.query(Company).filter_by(name="DCP").first()
    
    print("\n1. TESTING BASIC RELATIONSHIPS")
    print("-" * 40)
    
    # Test Freebie relationships
    print("Testing Freebie.dev and Freebie.company:")
    freebie = session.query(Freebie).filter_by(item_name="ODM T-shirts").first()
    print(f"  Freebie '{freebie.item_name}' belongs to dev: {freebie.dev.name}")
    print(f"  Freebie '{freebie.item_name}' belongs to company: {freebie.company.name}")
    
    # Test Company.freebies
    print(f"\nTesting Company.freebies:")
    print(f"  ODM freebies: {[f.item_name for f in odm.freebies]}")
    print(f"  UDA freebies: {[f.item_name for f in uda.freebies]}")
    print(f"  DCP freebies: {[f.item_name for f in dcp.freebies]}")
    
    # Test Dev.freebies
    print(f"\nTesting Dev.freebies:")
    print(f"  Raila's freebies: {[f.item_name for f in raila.freebies]}")
    print(f"  Ruto's freebies: {[f.item_name for f in ruto.freebies]}")
    print(f"  Rigachi's freebies: {[f.item_name for f in rigachi.freebies]}")
    
    # Test Company.devs (many-to-many through freebies)
    print(f"\nTesting Company.devs:")
    print(f"  ODM devs: {[d.name for d in odm.devs]}")
    print(f"  UDA devs: {[d.name for d in uda.devs]}")
    print(f"  DCP devs: {[d.name for d in dcp.devs]}")
    
    # Test Dev.companies (many-to-many through freebies)
    print(f"\nTesting Dev.companies:")
    print(f"  Raila's companies: {[c.name for c in raila.companies]}")
    print(f"  Ruto's companies: {[c.name for c in ruto.companies]}")
    print(f"  Rigachi's companies: {[c.name for c in rigachi.companies]}")
    
    print("\n2. TESTING FREEBIE METHODS")
    print("-" * 40)
    
    # Test Freebie.print_details()
    print("Testing Freebie.print_details():")
    for freebie in session.query(Freebie).limit(3):
        print(f"  {freebie.print_details()}")
    
    print("\n3. TESTING COMPANY METHODS")
    print("-" * 40)
    
    # Test Company.give_freebie()
    print("Testing Company.give_freebie():")
    new_freebie = odm.give_freebie(rigachi, "ODM Cap", 50000)
    session.add(new_freebie)
    session.commit()
    print(f"  Created new freebie: {new_freebie.print_details()}")
    
    # Test Company.oldest_company()
    print("\nTesting Company.oldest_company():")
    oldest = Company.oldest_company()
    print(f"  Oldest company: {oldest.name} (founded {oldest.founding_year})")
    
    print("\n4. TESTING DEV METHODS")
    print("-" * 40)
    
    # Test Dev.received_one()
    print("Testing Dev.received_one():")
    print(f"  Raila received 'ODM T-shirts': {raila.received_one('ODM T-shirts')}")
    print(f"  Raila received 'Laptop': {raila.received_one('Laptop')}")
    print(f"  Ruto received 'Wheelbarrow': {ruto.received_one('Wheelbarrow')}")
    print(f"  Ruto received 'ODM T-shirts': {ruto.received_one('ODM T-shirts')}")
    
    # Test Dev.give_away()
    print("\nTesting Dev.give_away():")
    wheelbarrow = session.query(Freebie).filter_by(item_name="Wheelbarrow").first()
    print(f"  Before: Wheelbarrow belongs to {wheelbarrow.dev.name}")
    
    success = ruto.give_away(rigachi, wheelbarrow)
    session.commit()
    print(f"  Give away successful: {success}")
    print(f"  After: Wheelbarrow belongs to {wheelbarrow.dev.name}")
    
    # Test giving away freebie that doesn't belong to dev
    odm_tshirt = session.query(Freebie).filter_by(item_name="ODM T-shirts").first()
    failed_attempt = ruto.give_away(rigachi, odm_tshirt)
    print(f"  Ruto trying to give away Raila's T-shirt: {failed_attempt}")
    
    print("\n5. TESTING AGGREGATE DATA")
    print("-" * 40)
    
    # Show summary statistics
    total_companies = session.query(Company).count()
    total_devs = session.query(Dev).count()
    total_freebies = session.query(Freebie).count()
    
    print(f"Total companies: {total_companies}")
    print(f"Total devs: {total_devs}")
    print(f"Total freebies: {total_freebies}")
    
    # Show value statistics
    total_value = sum(f.value for f in session.query(Freebie).all())
    print(f"Total value of all freebies: KSh {total_value:,}")
    
    # Show most valuable freebie
    most_valuable = session.query(Freebie).order_by(Freebie.value.desc()).first()
    print(f"Most valuable freebie: {most_valuable.item_name} (KSh {most_valuable.value:,})")
    
    print("\n6. TESTING EDGE CASES")
    print("-" * 40)
    
    # Test empty relationships
    new_company = Company(name="Test Company", founding_year=2024)
    session.add(new_company)
    session.commit()
    print(f"New company freebies: {len(new_company.freebies)}")
    print(f"New company devs: {len(new_company.devs)}")
    
    session.close()
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == '__main__':
    # Run the tests first
    test_relationships_and_methods()
    
    # Then start the interactive session
    print("\nStarting interactive debug session...")
    print("Available objects: Company, Dev, Freebie")
    print("Sample usage:")
    print("  session = sessionmaker(bind=create_engine('sqlite:///lib/freebies.db'))()")
    print("  raila = session.query(Dev).filter_by(name='Raila').first()")
    print("  print(raila.freebies)")
    print("\n" + "-" * 60)
    
    engine = create_engine('sqlite:///lib/freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Make some common objects available in the debug session
    raila = session.query(Dev).filter_by(name="Raila").first()
    ruto = session.query(Dev).filter_by(name="Ruto").first()
    rigachi = session.query(Dev).filter_by(name="Rigachi").first()
    
    odm = session.query(Company).filter_by(name="ODM").first()
    uda = session.query(Company).filter_by(name="UDA").first()
    dcp = session.query(Company).filter_by(name="DCP").first()
    
    import ipdb; ipdb.set_trace()