# Phase 3 Mock Code Challenge: Freebie Tracker

## Learning Goals

- Write SQLAlchemy migrations.
- Connect between tables using SQLAlchemy relationships.
- Use SQLAlchemy to run CRUD statements in the database.

***

## Key Vocab

- **Schema**: the blueprint of a database. Describes how data relates to other
  data in tables, columns, and relationships between them.
- **Persist**: save a schema in a database.
- **Engine**: a Python object that translates SQL to Python and vice-versa.
- **Session**: a Python object that uses an engine to allow us to
  programmatically interact with a database.
- **Transaction**: a strategy for executing database statements such that
  the group succeeds or fails as a unit.
- **Migration**: the process of moving data from one or more databases to one
  or more target databases.
  
***

## Introduction

For this assignment, we'll be working with a freebie domain.

As developers, when you attend hackathons, you'll realize they hand out a lot of
free items (informally called _freebies_, or swag)! Let's make an app for
developers that keeps track of all the freebies they obtain.

We have three models: `Company`, `Dev`, and `Freebie`

For our purposes, a `Company` has many `Freebie`s, a `Dev` has many `Freebie`s,
and a `Freebie` belongs to a `Dev` and to a `Company`.

`Company` - `Dev` is a many to many relationship.

**Note**: You should draw your domain on paper or on a whiteboard _before you
start coding_. Remember to identify a single source of truth for your data.

## Instructions

To get started, run `pipenv install && pipenv shell` while inside of this
directory.

Build out all of the methods listed in the deliverables. The methods are listed
in a suggested order, but you can feel free to tackle the ones you think are
easiest. Be careful: some of the later methods rely on earlier ones.

**Remember!** This mock code challenge does not have tests. You cannot run
`pytest` and you cannot run `learn test`. You'll need to create your own sample
instances so that you can try out your code on your own. Make sure your
relationships and methods work in the console before submitting.

We've provided you with a tool that you can use to test your code. To use it,
run `python debug.py` from the command line. This will start an `ipdb` session
with your classes defined. You can test out the methods that you write here. You
are also encouraged to use the `seed.py` file to create sample data to test your
models and associations.

Writing error-free code is more important than completing all of the
deliverables listed- prioritize writing methods that work over writing more
methods that don't work. You should test your code in the console as you write.

Similarly, messy code that works is better than clean code that doesn't. First,
prioritize getting things working. Then, if there is time at the end, refactor
your code to adhere to best practices.

**Before you submit!** Save and run your code to verify that it works as you
expect. If you have any methods that are not working yet, feel free to leave
comments describing your progress.

***

## What You Already Have

The starter code has migrations and models for the initial `Company` and `Dev`
models, and seed data for some `Company`s and `Dev`s. The schema currently looks
like this:

### companies Table

| Column        | Type    |
| ------------- | ------- |
| name          | String  |
| founding_year | Integer |

### devs Table

| Column | Type   |
| ------ | ------ |
| name   | String |

You will need to create the migration for the `freebies` table using the
attributes specified in the deliverables below.

***

## Deliverables

Write the following methods in the classes in the files provided. Feel free to
build out any helper methods if needed.

Remember: SQLAlchemy gives your classes access to a lot of methods already!
Keep in mind what methods SQLAlchemy gives you access to on each of your
classes when you're approaching the deliverables below.

### Migrations

Before working on the rest of the deliverables, you will need to create a
migration for the `freebies` table.

- A `Freebie` belongs to a `Dev`, and a `Freebie` also belongs to a `Company`.
  In your migration, create any columns your `freebies` table will need to
  establish these relationships using the right foreign keys.
- The `freebies` table should also have:
  - An `item_name` column that stores a string.
  - A `value` column that stores an integer.

After creating the `freebies` table using a migration, use the `seed.py` file to
create instances of your `Freebie` class so you can test your code.

**After you've set up your `freebies` table**, work on building out the following
deliverables.

### Relationship Attributes and Methods

Use SQLAlchemy's `ForeignKey`, `relationship()`, and `backref()` objects to
build relationships between your three models.

**Note**: The plural of "freebie" is "freebies" and the singular of "freebies"
is "freebie".

#### Freebie

- `Freebie.dev` returns the `Dev` instance for this Freebie.
- `Freebie.company` returns the `Company` instance for this Freebie.

#### Company

- `Company.freebies` returns a collection of all the freebies for the Company.
- `Company.devs` returns a collection of all the devs who collected freebies
  from the company.

#### Dev

- `Dev.freebies` returns a collection of all the freebies that the Dev has collected.
- `Dev.companies`returns a collection of all the companies that the Dev has collected
  freebies from.

Use `python debug.py` and check that these methods work before proceeding. For
example, you should be able to retrieve a dev from the database by its
attributes and view their companies with `dev.companies` (based on your seed
data).

### Aggregate Methods

#### Freebie

- `Freebie.print_details()`should return a string formatted as follows:
  `{dev name} owns a {freebie item_name} from {company name}`.

#### Company

- `Company.give_freebie(dev, item_name, value)` takes a `dev` (an instance of
  the `Dev` class), an `item_name` (string), and a `value` as arguments, and
  creates a new `Freebie` instance associated with this company and the given
  dev.
- Class method `Company.oldest_company()`returns the `Company` instance with
  the earliest founding year.

#### Dev

- `Dev.received_one(item_name)` accepts an `item_name` (string) and returns
  `True` if any of the freebies associated with the dev has that `item_name`,
  otherwise returns `False`.
- `Dev.give_away(dev, freebie)` accepts a `Dev` instance and a `Freebie`
  instance, changes the freebie's dev to be the given dev; your code should only
  make the change if the freebie belongs to the dev who's giving it away

## Setup Instructions

### 1. Install Dependencies

```bash
# Navigate to project directory
cd ***

# Install required packages
pipenv install
pipenv shell

# Or using pip
pip install sqlalchemy alembic
```

### 2. Database Setup

```bash
# Navigate to lib directory
cd lib
# Run database migration
alembic revision -m "create freebies table"
alembic upgrade head

# Create sample data
python seed.py
```

## Running the Application

### 1. Test Relationships and Methods

```bash
# From lib directory
python debug.py
```

**Expected Output:**
-  All relationship tests passed
-  All method implementations working
-  Interactive ipdb session starts

### 2. SQL Join Demonstrations

```bash
# From project root directory
python lib/Joins_delete/sqlite_joins.py
```

**Shows:**
- INNER JOIN examples
- LEFT JOIN patterns
- GROUP BY aggregations
- WHERE filtering

### 3. Database Management

```bash
# Delete specific company
python lib/Joins_delete/delete_company.py

# Check database status
python -c "
import sqlite3
conn = sqlite3.connect('lib/freebies.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM companies')
print(f'Companies: {cursor.fetchone()[0]}')
cursor.execute('SELECT COUNT(*) FROM devs')
print(f'Devs: {cursor.fetchone()[0]}')
cursor.execute('SELECT COUNT(*) FROM freebies')
print(f'Freebies: {cursor.fetchone()[0]}')
conn.close()
"
```

## Key Features

### Models and Relationships

- **Company**: Has many freebies, connects to devs through freebies
- **Dev**: Has many freebies, connects to companies through freebies  
- **Freebie**: Belongs to both a dev and a company

### Available Methods

#### Freebie Methods
```python
freebie.print_details()  # Returns formatted string
```

#### Company Methods
```python
company.give_freebie(dev, item_name, value)  # Creates new freebie
Company.oldest_company()  # Class method returns oldest company
```

#### Dev Methods
```python
dev.received_one(item_name)  # Returns True/False
dev.give_away(other_dev, freebie)  # Transfers freebie ownership
```

## Sample Data

The seed script creates:

| Company | Founded | Freebies Given |
|---------|---------|----------------|
| ODM     | 2005    | 2              |
| UDA     | 2022    | 2              |
| DCP     | 2025    | 1              |

| Developer | Freebies Received | Total Value |
|-----------|-------------------|-------------|
| Raila     | 2                 | KSh 7,500,000 |
| Ruto      | 2                 | KSh 1,800,000 |
| Rigachi   | 1                 | KSh 500,000   |

## Testing Commands

### Quick Database Check
```bash
# From lib directory
sqlite3 freebies.db "SELECT * FROM companies;"
sqlite3 freebies.db "SELECT * FROM devs;"
sqlite3 freebies.db "SELECT * FROM freebies;"
```

### Test Specific Relationships
```python
# In debug.py ipdb session
raila = session.query(Dev).filter_by(name="Raila").first()
print(raila.freebies)  # Show Raila's freebies
print(raila.companies)  # Show companies Raila got freebies from

odm = session.query(Company).filter_by(name="ODM").first()
print(odm.freebies)  # Show ODM's freebies
print(odm.devs)  # Show devs who got freebies from ODM
```

### Test Methods
```python
# Test freebie details
freebie = session.query(Freebie).first()
print(freebie.print_details())

# Test company methods
odm.give_freebie(rigachi, "ODM Cap", 50000)
oldest = Company.oldest_company()

# Test dev methods
raila.received_one("ODM T-shirts")  # Should return True
ruto.give_away(rigachi, wheelbarrow_freebie)
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'models'**
   ```bash
   # Make sure you're in the lib directory
   cd lib
   python debug.py
   ```

2. **sqlite3.OperationalError: no such table: freebies**
   ```bash
   # Run the migration first
   alembic upgrade head
   ```

3. **No data in database**
   ```bash
   # Create sample data
   python seed.py
   ```

### Reset Database
```bash
# From lib directory
rm freebies.db
alembic upgrade head
python seed.py
```

## SQL Join Examples

The project demonstrates these essential join patterns:

1. **INNER JOIN** - Match records in both tables
2. **LEFT JOIN** - Include all records from left table
3. **GROUP BY** - Aggregate data across tables
4. **WHERE** - Filter joined results

Run `python lib/Joins_delete/sqlite_joins.py` to see examples.

## Assignment Deliverables

 **Migrations**: Created freebies table with foreign keys  
 **Relationships**: All models have correct SQLAlchemy relationships  
 **Freebie methods**: `print_details()` implemented  
 **Company methods**: `give_freebie()` and `oldest_company()` working  
 **Dev methods**: `received_one()` and `give_away()` functional  
 **Testing**: Comprehensive test suite in debug.py

## Next Steps

1. Run all tests: `python debug.py`
2. Explore joins: `python lib/Joins_delete/sqlite_joins.py`
3. Test edge cases in the interactive session
4. Add more complex queries and relationships

---

**Note**: This project uses a political theme for sample data (ODM, UDA, DCP parties with Raila, Ruto, Rigathi as developers) for educational purposes.
```
