import sqlite3
import os

# Replace 'mydatabase.db' with the desired filename for your SQLite database
db_file = 'mockdb.db'

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
# Connect to the database (this will create the file if it doesn't exist)
conn = sqlite3.connect(db_file)

# Create a cursor object to interact with the database
cursor = conn.cursor()

query = f"SELECT * FROM {'aluno'} WHERE registro = ?"# AND senha = ?"

# Execute the query with parameters
cursor.execute(query, (1))#, 'admin'))

admin = cursor.fetchone()
print(type(admin))
print(admin)

# Commit the changes and close the database connection
conn.commit()
conn.close()

import secrets

secret_key = secrets.token_hex(16)  # This will give you a 32 characters long string
print(secret_key)


print(f"All good boy'o")