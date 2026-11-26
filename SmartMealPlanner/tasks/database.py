import mariadb
from contextlib import contextmanager


DB_CONFIG = {
    "user": "luoton",
    "database": "smartmeal",
    "unix_socket": "/tmp/mysql.sock"
}


@contextmanager
def get_connection():
    conn = mariadb.connect(**DB_CONFIG)

    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_database():
    with get_connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ingredients (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    quantity DECIMAL(12,3) NOT NULL,
                    unit VARCHAR(30) NOT NULL,
                    CONSTRAINT chk_quantity CHECK (quantity >= 0)
                )
            """)

            conn.commit()
        finally:
            cursor.close()

    print("MariaDB initialized successfully!")