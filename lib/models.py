from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
import os

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    # Relationship to freebies
    freebies = relationship('Freebie', back_populates='company')

    def __repr__(self):
        return f'<Company {self.name}>'

    # Aggregate Methods
    def give_freebie(self, dev, item_name, value):
        """Creates a new Freebie associated with this company and the given dev"""
        # Create new freebie
        new_freebie = Freebie(
            item_name=item_name,
            value=value,
            dev=dev,
            company=self
        )
        return new_freebie

    @classmethod
    def oldest_company(cls):
        """Returns the Company instance with the earliest founding year"""
        # Fix database path - use current directory
        db_path = os.path.join(os.path.dirname(__file__), 'freebies.db')
        engine = create_engine(f'sqlite:///{db_path}')
        Session = sessionmaker(bind=engine)
        session = Session()
        
        oldest = session.query(cls).order_by(cls.founding_year.asc()).first()
        session.close()
        return oldest

    @property
    def devs(self):
        """Returns a collection of all devs who collected freebies from the company"""
        return list(set([freebie.dev for freebie in self.freebies]))


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    # Relationship to freebies
    freebies = relationship('Freebie', back_populates='dev')

    def __repr__(self):
        return f'<Dev {self.name}>'

    @property
    def companies(self):
        """Returns a collection of all companies that the Dev has collected freebies from"""
        return list(set([freebie.company for freebie in self.freebies]))

    # Aggregate Methods
    def received_one(self, item_name):
        """Returns True if any of the freebies associated with the dev has that item_name"""
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        """Changes the freebie's dev to be the given dev if the freebie belongs to this dev"""
        if freebie in self.freebies:
            freebie.dev = dev
            return True
        return False


class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String(), nullable=False)
    value = Column(Integer(), nullable=False)
    
    # Foreign Keys
    dev_id = Column(Integer(), ForeignKey('devs.id'), nullable=False)
    company_id = Column(Integer(), ForeignKey('companies.id'), nullable=False)

    # Relationships
    dev = relationship('Dev', back_populates='freebies')
    company = relationship('Company', back_populates='freebies')

    def __repr__(self):
        return f'<Freebie {self.item_name}>'

    def print_details(self):
        """Returns a formatted string with freebie details"""
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"


# Test the models if run directly
if __name__ == "__main__":
    print(" Models loaded successfully!")
    print("Available models: Company, Dev, Freebie")
    
    # Test database connection
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'freebies.db')
        engine = create_engine(f'sqlite:///{db_path}')
        
        # Test if we can connect
        with engine.connect() as conn:
            print(f" Database connection successful: {db_path}")
            
        # Check if tables exist
        if os.path.exists(db_path):
            Session = sessionmaker(bind=engine)
            session = Session()
            
            try:
                company_count = session.query(Company).count()
                dev_count = session.query(Dev).count()
                freebie_count = session.query(Freebie).count()
                
                print(f" Current data:")
                print(f"   Companies: {company_count}")
                print(f"   Developers: {dev_count}")
                print(f"   Freebies: {freebie_count}")
                
                if company_count == 0:
                    print(" Run 'python seed.py' to add sample data")
                    
            except Exception as e:
                print(f"  Tables may not exist yet. Run 'alembic upgrade head' first")
            finally:
                session.close()
        else:
            print("  Database file doesn't exist. Run 'alembic upgrade head' and 'python seed.py'")
            
    except Exception as e:
        print(f" Database connection failed: {e}")