import mysql.connector

conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cli_todo"
    )
cursor = conn.cursor()

# Insert a user into the 'users' table
cursor.execute(
    """SELECT * FROM users WHERE name = %s AND password = %s""")
res = cursor.fetchone()
print(res)

# Commit changes and close connection
cursor.close()
conn.close()
