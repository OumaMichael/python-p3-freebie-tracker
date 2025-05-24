#!/usr/bin/env python3

# Script goes here!

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie, Base

# Create engine and session
engine = create_engine('sqlite:///lib/freebies.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Clear existing data
session.query(Freebie).delete()
session.query(Company).delete()
session.query(Dev).delete()

# Create companies
google = Company(name="Google", founding_year=1998)
apple = Company(name="Apple", founding_year=1976)
microsoft = Company(name="Microsoft", founding_year=1975)

# Create devs
alice = Dev(name="Alice")
bob = Dev(name="Bob")
charlie = Dev(name="Charlie")

# Add to session
session.add_all([google, apple, microsoft, alice, bob, charlie])
session.commit()

# Create freebies
freebie1 = Freebie(item_name="T-shirt", value=25, dev=alice, company=google)
freebie2 = Freebie(item_name="Stickers", value=5, dev=alice, company=apple)
freebie3 = Freebie(item_name="Water Bottle", value=15, dev=bob, company=google)
freebie4 = Freebie(item_name="Laptop Bag", value=50, dev=charlie, company=microsoft)
freebie5 = Freebie(item_name="Pen", value=3, dev=bob, company=apple)

session.add_all([freebie1, freebie2, freebie3, freebie4, freebie5])
session.commit()

print("Seed data created successfully!")
print(f"Companies: {session.query(Company).count()}")
print(f"Devs: {session.query(Dev).count()}")
print(f"Freebies: {session.query(Freebie).count()}")

session.close()