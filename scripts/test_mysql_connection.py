"""Test connectivity to a local MySQL server using credentials from the environment.

Usage:
    1. Copy .env.example to .env and fill in your MySQL credentials.
    2. pip install -r requirements.txt
    3. python scripts/test_mysql_connection.py
"""

import os
import sys

from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

REQUIRED_VARS = ["MYSQL_HOST", "MYSQL_USER", "MYSQL_PASSWORD"]


def get_config():
    missing = [var for var in REQUIRED_VARS if not os.getenv(var)]
    if missing:
        print(f"Missing required environment variables: {', '.join(missing)}")
        print("Copy .env.example to .env and fill in your MySQL credentials.")
        sys.exit(1)

    return {
        "host": os.getenv("MYSQL_HOST"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": os.getenv("MYSQL_DATABASE") or None,
    }


def main():
    config = get_config()
    connection = None
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            server_info = connection.get_server_info()
            print(f"Connected to MySQL server version {server_info}")

            cursor = connection.cursor()
            if config["database"]:
                cursor.execute("SHOW TABLES;")
                tables = [row[0] for row in cursor.fetchall()]
                print(f"Tables in '{config['database']}' ({len(tables)}):")
                for table in tables:
                    print(f"  - {table}")
            else:
                cursor.execute("SHOW DATABASES;")
                databases = [row[0] for row in cursor.fetchall()]
                print(f"No MYSQL_DATABASE set. Databases visible on this server ({len(databases)}):")
                for db in databases:
                    print(f"  - {db}")
                print("Set MYSQL_DATABASE in .env to list tables within one of them.")
            cursor.close()
    except Error as e:
        print(f"Failed to connect to MySQL: {e}")
        sys.exit(1)
    finally:
        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    main()
