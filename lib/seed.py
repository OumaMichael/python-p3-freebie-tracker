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
ODM = Company(name="ODM", founding_year=2005)
UDA = Company(name="UDA", founding_year=2022)
DCP = Company(name="DCP", founding_year=2025)

# Create devs
Raila = Dev(name="Raila")
Ruto = Dev(name="Ruto")
Rigachi = Dev(name="Rigachi")

# Add to session
session.add_all([ODM, UDA, DCP, Raila, Ruto, Rigachi])
session.commit()

# Create freebies
freebie1 = Freebie(item_name="ODM T-shirts", value=2500000, dev=Raila, company=ODM)
freebie2 = Freebie(item_name="CDF funds", value=5000000, dev=Raila, company=UDA)
freebie3 = Freebie(item_name="Hustler funds", value=1500000, dev=Ruto, company=ODM)
freebie4 = Freebie(item_name="DCP Tanks", value=500000, dev=Rigachi, company=DCP)
freebie5 = Freebie(item_name="Wheelbarrow", value=300000, dev=Ruto, company=UDA)

session.add_all([freebie1, freebie2, freebie3, freebie4, freebie5])
session.commit()

print("Seed data created successfully!")
print(f"Companies: {session.query(Company).count()}")
print(f"Devs: {session.query(Dev).count()}")
print(f"Freebies: {session.query(Freebie).count()}")

session.close()