import mysql.connector

config = {
    "host": "localhost",
    "user": "root",
    "password": "Stalker2007+",
    "database": "cinema",
}


def create_connection():
    try:
        connection = mysql.connector.connect(**config)

        return connection
    except mysql.connector.Error as err:
        print(f"Error when connection to database: {err}")
        return None
