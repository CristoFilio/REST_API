import sqlite3

connection = sqlite3.Connection('data.db')
cursor = connection.cursor()
#Add Tables
# create_user_table = 'CREATE TABLE IF NOT EXISTS users ' \
#                     '(id INTEGER PRIMARY KEY, username text,' \
#                     ' password text, access int)'
# create_item_table = 'CREATE TABLE IF NOT EXISTS items ' \
#                     '(id INTEGER PRIMARY KEY, name text, price real)'

# cursor.execute(create_user_table)
# cursor.execute(create_item_table)

# Create User
# user = (1, 'cris', 'pass', 5)
# create_user = 'INSERT INTO users VALUES (?, ?, ?, ?)'
# cursor.execute(create_user, user)
name = 'tv'
data = 9.99
cursor.execute(f"INSERT INTO items VALUES (NULL, '{name}', {data})")
# Print Users
# users = [user for user in cursor.execute('SELECT * FROM users')]
# print(users)

connection.commit()
connection.close()
