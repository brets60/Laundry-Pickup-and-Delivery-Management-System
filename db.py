import os
import re
import sqlite3
import datetime
from decimal import Decimal

DATABASE_URL = os.environ.get("DATABASE_URL", "")
DEFAULT_SQLITE_DB = os.environ.get("DATABASE", "laundry.db")

def is_postgres():
    target = os.environ.get("DATABASE_URL", DATABASE_URL).strip()
    return target.startswith("postgres://") or target.startswith("postgresql://")

def normalize_supabase_url(url):
    """
    Supabase direct connections (db.[ref].supabase.co:5432) only provide IPv6 DNS.
    Render and many cloud hosts do not support IPv6 outbound connections.
    This helper automatically translates direct URLs to the Supabase IPv4 Pooler URL.
    """
    trimmed = url.strip()
    if trimmed.startswith("postgres://"):
        trimmed = trimmed.replace("postgres://", "postgresql://", 1)

    m = re.match(r'postgresql://([^:]+):([^@]+)@db\.([a-zA-Z0-9]+)\.supabase\.co:5432/(.+)', trimmed)
    if m:
        user, pw, ref, dbname = m.groups()
        pooler_user = f"{user}.{ref}" if "." not in user else user
        return f"postgresql://{pooler_user}:{pw}@aws-0-ap-southeast-1.pooler.supabase.com:5432/{dbname}"
    return trimmed


class PostgresRowWrapper(dict):
    def __init__(self, raw_row, cursor_description):
        super().__init__()
        self._keys = [d[0] for d in cursor_description]
        for i, key in enumerate(self._keys):
            val = raw_row[i]
            if isinstance(val, (datetime.datetime, datetime.date)):
                val = str(val)
            elif isinstance(val, Decimal):
                val = float(val)
            self[key] = val

    def __getitem__(self, key):
        if isinstance(key, int):
            return self[self._keys[key]]
        return super().__getitem__(key)

    def keys(self):
        return self._keys


class PostgresCursorWrapper:
    def __init__(self, cursor):
        self._cur = cursor
        self.lastrowid = None
        self.rowcount = -1

    @property
    def description(self):
        return self._cur.description

    def _convert_query(self, sql):
        trimmed = sql.strip().rstrip(';')
        if trimmed.upper().startswith("PRAGMA"):
            return None, False

        # Convert '?' placeholders to '%s'
        converted_sql = re.sub(r'\?', '%s', trimmed)

        is_insert = converted_sql.strip().upper().startswith("INSERT INTO")
        has_returning = "RETURNING" in converted_sql.upper()
        if is_insert and not has_returning:
            converted_sql += " RETURNING id"
            return converted_sql, True

        return converted_sql, False

    def execute(self, sql, params=None):
        converted_sql, has_added_returning = self._convert_query(sql)
        if converted_sql is None:
            return self

        try:
            if params is None:
                self._cur.execute(converted_sql)
            else:
                self._cur.execute(converted_sql, params)
            
            self.rowcount = self._cur.rowcount

            if has_added_returning:
                try:
                    row = self._cur.fetchone()
                    if row:
                        self.lastrowid = row[0]
                except Exception:
                    self.lastrowid = None
        except Exception as e:
            if has_added_returning:
                fallback_sql = converted_sql.rsplit(" RETURNING id", 1)[0]
                if params is None:
                    self._cur.execute(fallback_sql)
                else:
                    self._cur.execute(fallback_sql, params)
                self.rowcount = self._cur.rowcount
            else:
                raise e

        return self

    def fetchone(self):
        try:
            row = self._cur.fetchone()
            if row is None:
                return None
            return PostgresRowWrapper(row, self._cur.description)
        except Exception:
            return None

    def fetchall(self):
        try:
            rows = self._cur.fetchall()
            if not rows:
                return []
            desc = self._cur.description
            return [PostgresRowWrapper(r, desc) for r in rows]
        except Exception:
            return []

    def close(self):
        try:
            self._cur.close()
        except Exception:
            pass

    def __iter__(self):
        while True:
            row = self.fetchone()
            if row is None:
                break
            yield row


class PostgresConnectionWrapper:
    def __init__(self, raw_conn):
        self._conn = raw_conn
        self.row_factory = None
        self.total_changes = 0

    def cursor(self):
        cur = self._conn.cursor()
        return PostgresCursorWrapper(cur)

    def execute(self, sql, params=None):
        cur = self.cursor()
        return cur.execute(sql, params)

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        self._conn.close()


def get_sqlite_fallback(database_path=None):
    target_file = database_path or DEFAULT_SQLITE_DB
    conn = sqlite3.connect(target_file)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def get_db_connection(database_path=None):
    db_target = os.environ.get("DATABASE_URL", DATABASE_URL).strip()
    
    if db_target.startswith("postgres://") or db_target.startswith("postgresql://"):
        import psycopg2
        normalized_url = normalize_supabase_url(db_target)
        try:
            raw_conn = psycopg2.connect(normalized_url, connect_timeout=6)
            return PostgresConnectionWrapper(raw_conn)
        except Exception as err:
            print(f"[Database Connection Warning] Failed to connect to PostgreSQL ({err}). Falling back to SQLite.")
            return get_sqlite_fallback(database_path)
    else:
        return get_sqlite_fallback(database_path)
