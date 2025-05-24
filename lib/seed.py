#!/usr/bin/env python3

# Script goes here!

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie, Base
import os

# Create engine and session - fix the database path
# Since we're running from lib directory, database should be in current directory
db_path = os.path.join(os.path.dirname(__file__), 'freebies.db')
engine = create_engine(f'sqlite:///{db_path}')

# Create all tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

print("Database connection established successfully!")
print(f"Database location: {db_path}")

try:
    # Clear existing data
    print("Clearing existing data...")
    session.query(Freebie).delete()
    session.query(Company).delete()
    session.query(Dev).delete()
    session.commit()

    # Create companies
    print("Creating companies...")
    ODM = Company(name="ODM", founding_year=2005)
    UDA = Company(name="UDA", founding_year=2022)
    DCP = Company(name="DCP", founding_year=2025)

    # Create devs
    print("Creating developers...")
    Raila = Dev(name="Raila")
    Ruto = Dev(name="Ruto")
    Rigachi = Dev(name="Rigachi")

    # Add to session
    session.add_all([ODM, UDA, DCP, Raila, Ruto, Rigachi])
    session.commit()
    print("Companies and developers added successfully!")

    # Create freebies
    print("Creating freebies...")
    freebie1 = Freebie(item_name="ODM T-shirts", value=2500000, dev=Raila, company=ODM)
    freebie2 = Freebie(item_name="CDF funds", value=5000000, dev=Raila, company=UDA)
    freebie3 = Freebie(item_name="Hustler funds", value=1500000, dev=Ruto, company=ODM)
    freebie4 = Freebie(item_name="DCP Tanks", value=500000, dev=Rigachi, company=DCP)
    freebie5 = Freebie(item_name="Wheelbarrow", value=300000, dev=Ruto, company=UDA)
    freebie6 = Freebie(item_name="ODM Banners", value=1000000, dev=Raila, company=ODM)

    session.add_all([freebie1, freebie2, freebie3, freebie4, freebie5, freebie6])
    session.commit()

    print("\n" + "=" * 50)
    print(" SEED DATA CREATED SUCCESSFULLY!")
    print("=" * 50)
    print(f"Companies: {session.query(Company).count()}")
    print(f"Devs: {session.query(Dev).count()}")
    print(f"Freebies: {session.query(Freebie).count()}")
    
    # Show the data that was created
    print("\nCreated Companies:")
    for company in session.query(Company).all():
        print(f"  - {company.name} (Founded: {company.founding_year})")
    
    print("\nCreated Developers:")
    for dev in session.query(Dev).all():
        print(f"  - {dev.name}")
    
    print("\nCreated Freebies:")
    for freebie in session.query(Freebie).all():
        print(f"  - {freebie.item_name}: KSh {freebie.value:,} ({freebie.dev.name} from {freebie.company.name})")
    
    total_value = sum(f.value for f in session.query(Freebie).all())
    print(f"\nTotal value of all freebies: KSh {total_value:,}")

except Exception as e:
    print(f" Error creating seed data: {e}")
    session.rollback()
finally:
    session.close()