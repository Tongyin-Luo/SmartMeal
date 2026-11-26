from tasks.database import get_connection


def main():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT VERSION()")
            print("MariaDB Version:", cursor.fetchone()[0])

            cursor.execute("SELECT CURRENT_USER()")
            print("Connected User:", cursor.fetchone()[0])

            cursor.execute("SELECT DATABASE()")
            print("Database:", cursor.fetchone()[0])

            cursor.close()

        print("Connection successful!")

    except Exception as e:
        print("Connection failed:", e)


if __name__ == "__main__":
    main()