import sqlite3
import os

# Replace 'mydatabase.db' with the desired filename for your SQLite database
db_file = 'mockdb.db'
sql_file = 'db_creation_template.sql'

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
# Connect to the database (this will create the file if it doesn't exist)
conn = sqlite3.connect(db_file)

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Define the SQL command to create a table
def executeScriptsFromFile(filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')
    print(len(sqlCommands))
    iteration = 1
    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            cursor.execute(command)
        except Exception as e:
            print(f"Command skipped: {iteration} - ",  e)
        iteration+=1
# Execute the SQL command to create the table

executeScriptsFromFile(filename=os.path.join(__location__, sql_file))

# Commit the changes and close the database connection
conn.commit()
conn.close()

print(f"All good boy'o")