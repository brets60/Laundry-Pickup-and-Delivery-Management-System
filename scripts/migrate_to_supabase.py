import sqlite3
import psycopg2

SQLITE_PATH = "laundry.db"
SUPABASE_URL = "postgresql://postgres:bretania200419@db.uzzqfapcafztnfvbpolt.supabase.co:5432/postgres"

def migrate():
    sqlite_conn = sqlite3.connect(SQLITE_PATH)
    sqlite_conn.row_factory = sqlite3.Row
    
    pg_conn = psycopg2.connect(SUPABASE_URL)
    pg_cur = pg_conn.cursor()

    tables = [
        "users",
        "staff_members",
        "customers",
        "laundry_orders",
        "pickup_schedules",
        "delivery_records",
        "payments",
        "notifications"
    ]

    for table in tables:
        print(f"Migrating {table}...")
        sqlite_cur = sqlite_conn.execute(f"SELECT * FROM {table}")
        rows = sqlite_cur.fetchall()
        if not rows:
            print(f"  No rows in {table}.")
            continue

        cols = [k for k in rows[0].keys()]
        placeholders = ", ".join(["%s"] * len(cols))
        col_names = ", ".join(cols)

        # Clear existing in PG (or truncate with cascade)
        pg_cur.execute(f"TRUNCATE TABLE {table} CASCADE;")

        insert_sql = f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})"
        for row in rows:
            vals = [row[c] for c in cols]
            pg_cur.execute(insert_sql, vals)

        # Reset sequence to max id
        if "id" in cols:
            pg_cur.execute(f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), coalesce(max(id), 1), max(id) IS NOT NULL) FROM {table};")

        print(f"  Migrated {len(rows)} rows into {table}.")

    pg_conn.commit()
    pg_conn.close()
    sqlite_conn.close()
    print("Migration to Supabase completed successfully!")

if __name__ == "__main__":
    migrate()
