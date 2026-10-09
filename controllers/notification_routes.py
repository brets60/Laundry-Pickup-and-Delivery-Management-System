import os
import sqlite3
from flask import Blueprint, jsonify, request, session, render_template, redirect
from controllers.notification_service import (
    add_notification,
    get_recent_notifications,
    count_unread_notifications
)

notification_bp = Blueprint('notification', __name__)
DATABASE = os.environ.get("DATABASE", "laundry.db")


from db import get_db_connection


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
            # First poll for this session: if there are unread notifications, surface the latest one
            rows = conn.execute("""
                SELECT id, title, message, type, reference_id, reference_type, is_read, created_at
                FROM notifications
                WHERE is_read = 0
                ORDER BY id DESC
                LIMIT 1
            """).fetchall()
            new_notifs = [dict(r) for r in rows]

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


@notification_bp.route('/notifications-page')
def notifications_page():
    if "user_id" not in session:
        return redirect('/login')

    conn = get_db_connection()
    try:
        notifs = get_recent_notifications(conn, limit=100)
        unread = count_unread_notifications(conn)
        return render_template('notifications.html', notifications=notifs, unread_count=unread)
    finally:
        conn.close()
