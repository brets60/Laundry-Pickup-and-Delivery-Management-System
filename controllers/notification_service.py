"""
LaundryCare Notification Service
Centralized helper for creating and querying notifications when pickups
or deliveries are marked completed by motorcycle couriers.
"""
import sqlite3


def add_notification(conn, title, message, notif_type="info", reference_id=None, reference_type=None):
    """
    Inserts a new notification for shop staff into the database.
    """
    try:
        conn.execute("""
            INSERT INTO notifications (title, message, type, reference_id, reference_type, is_read, created_at)
            VALUES (?, ?, ?, ?, ?, 0, CURRENT_TIMESTAMP)
        """, (title, message, notif_type, reference_id, reference_type))
    except Exception as e:
        print(f"[NotificationService] Error creating notification: {e}")


def get_recent_notifications(conn, limit=20, unread_only=False):
    """
    Retrieves recent notifications ordered newest first.
    """
    try:
        if unread_only:
            rows = conn.execute("""
                SELECT id, title, message, type, reference_id, reference_type, is_read, created_at
                FROM notifications
                WHERE is_read = 0
                ORDER BY id DESC
                LIMIT ?
            """, (limit,)).fetchall()
        else:
            rows = conn.execute("""
                SELECT id, title, message, type, reference_id, reference_type, is_read, created_at
                FROM notifications
                ORDER BY id DESC
                LIMIT ?
            """, (limit,)).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"[NotificationService] Error fetching notifications: {e}")
        return []


def count_unread_notifications(conn):
    """
    Counts unread notifications.
    """
    try:
        row = conn.execute("SELECT COUNT(*) AS cnt FROM notifications WHERE is_read = 0").fetchone()
        return row['cnt'] if row else 0
    except Exception as e:
        return 0
