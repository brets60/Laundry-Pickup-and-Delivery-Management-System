import os
import sqlite3
from flask import Blueprint, jsonify, request, session
from controllers.notification_service import (
    add_notification,
    get_recent_notifications,
    count_unread_notifications
)

notification_bp = Blueprint('notification', __name__)
DATABASE = os.environ.get("DATABASE", "laundry.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


@notification_bp.route('/api/notifications', methods=['GET'])
def list_notifications():
    if "user_id" not in session:
        return jsonify({"status": 401, "error": "Unauthorized"}), 401

    conn = get_db_connection()
    try:
        limit = int(request.args.get('limit', 20))
        notifs = get_recent_notifications(conn, limit=limit)
        unread = count_unread_notifications(conn)
        return jsonify({
            "status": 200,
            "unread_count": unread,
            "notifications": notifs
        })
    finally:
        conn.close()


@notification_bp.route('/api/notifications/poll', methods=['GET'])
def poll_notifications():
    if "user_id" not in session:
        return jsonify({"status": 401, "error": "Unauthorized"}), 401

    conn = get_db_connection()
    try:
        last_id = int(request.args.get('last_id', 0))
        if last_id > 0:
            rows = conn.execute("""
                SELECT id, title, message, type, reference_id, reference_type, is_read, created_at
                FROM notifications
                WHERE id > ?
                ORDER BY id ASC
            """, (last_id,)).fetchall()
            new_notifs = [dict(r) for r in rows]
        else:
            new_notifs = []

        unread = count_unread_notifications(conn)
        recent = get_recent_notifications(conn, limit=10)
        return jsonify({
            "status": 200,
            "unread_count": unread,
            "new_notifications": new_notifs,
            "recent": recent
        })
    finally:
        conn.close()


@notification_bp.route('/api/notifications/mark-read', methods=['POST'])
def mark_notifications_read():
    if "user_id" not in session:
        return jsonify({"status": 401, "error": "Unauthorized"}), 401

    data = request.get_json() or {}
    notif_id = data.get('id')

    conn = get_db_connection()
    try:
        if notif_id:
            conn.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notif_id,))
        else:
            conn.execute("UPDATE notifications SET is_read = 1")
        conn.commit()
        unread = count_unread_notifications(conn)
        return jsonify({"status": 200, "unread_count": unread, "message": "Marked as read"})
    finally:
        conn.close()
