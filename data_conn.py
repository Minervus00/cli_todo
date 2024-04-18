import mysql.connector


# Function to create the database and tables if they don't exist
def create_database():
    # Connect to MySQL server
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
    cursor = conn.cursor()

    # Create the database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS cli_todo")

    # Connect to the newly created database
    conn.database = "cli_todo"

    # Create USERS table if it doesn't already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INT AUTO_INCREMENT PRIMARY KEY,
                      name VARCHAR(50),
                      email VARCHAR(25),
                      password VARCHAR(25),
                      admin TINYINT(1)
                   )''')

    # Create TASKS table if it doesn't already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                     (id INT AUTO_INCREMENT PRIMARY KEY,
                      titre VARCHAR(50) NOT NULL,
                      description TEXT,
                      fini TINYINT(1) NOT NULL DEFAULT 0,
                      userId INT NOT NULL
                  )''')

    # Commit changes and close connection
    conn.commit()
    conn.close()


def insert_user(name: str, email: str, passwd: str, admin: int):
    # Connect to MySQL server
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cli_todo"
    )
    cursor = conn.cursor()

    # Insert a user into the 'users' table
    cursor.execute(
        """INSERT INTO users (name, email, password, admin)
        VALUES (%s, %s, %s, %s)""",
        (name, email, passwd, admin))

    # Commit changes and close connection
    conn.commit()
    cursor.close()
    conn.close()


def search_user(name, passwd):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cli_todo"
    )
    cursor = conn.cursor()

    # Insert a user into the 'users' table
    cursor.execute(
        """SELECT * FROM users WHERE name = %s AND password = %s""",
        (name, passwd))
    res = cursor.fetchone()
    # print(res)

    cursor.close()
    conn.close()

    return res


def insert_tasks(titre: str, desc: str, done: int, id_user: int):
    # Connect to MySQL server
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cli_todo"
    )
    cursor = conn.cursor()

    # Insert a user into the 'tasks' table
    cursor.execute(
        """INSERT INTO tasks (titre, description, fini, userId)
        VALUES (%s, %s, %s, %s)""",
        (titre, desc, done, id_user))

    # Commit changes and close connection
    conn.commit()
    conn.close()


def list_tasks(id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cli_todo"
    )
    cursor = conn.cursor()

    # Insert a user into the 'users' table
    cursor.execute(
        """SELECT * FROM tasks WHERE userId = %s""",
        (id,))
    res = cursor.fetchall()
    # print(res)

    cursor.close()
    conn.close()

    return res


if __name__ == "__main__":
    # create_database()
    # insert_user("FuLLM374L", "full@metal.com", "N4vyS34l", 1)
    # resp = search_user("FuLLM374L", "N4vyS34l")
    # print(resp)
    # insert_tasks("push_up", "en faire 30 chaque jour", 0, 1)
    # insert_tasks("Arabic", "a lesson by day", 0, 1)
    # insert_tasks("Be happy", "Every single day", 1, 1)
    for t in list_tasks(3):
        print(t)
