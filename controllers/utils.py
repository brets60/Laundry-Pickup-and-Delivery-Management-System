"""
LaundryCare Central Utility Module (Week 11 Tech Debt Elimination)
Centralizes HTTP request detection, input sanitization, and security helpers
across all domain controllers.
"""

import re
from flask import request


def is_async_request() -> bool:
    """
    Standardized detector for asynchronous (Fetch/AJAX) requests.
    Inspects Content-Type, custom X-Requested-With headers, and Accept headers.
    """
    return bool(
        request.is_json
        or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        or 'application/json' in request.headers.get('Accept', '')
    )


def strip_html_tags(text: str) -> str:
    """
    Strips raw HTML tags, embedded scripts, and inline event handlers from inputs
    to prevent Stored XSS.
    Resolves BUG-001 (Triage Sprint).
    """
    if not text:
        return ""
    # Remove script blocks and their interior executable content
    clean = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', str(text), flags=re.IGNORECASE | re.DOTALL)
    # Remove style blocks and their interior styling
    clean = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', clean, flags=re.IGNORECASE | re.DOTALL)
    # Strip all other HTML tags
    clean = re.sub(r'<[^>]*?>', '', clean)
    # Escape any lingering raw angle brackets
    clean = clean.replace('<', '&lt;').replace('>', '&gt;')
    return clean.strip()


def sanitize_text(text: str, max_len: int = 500) -> str:
    """
    Sanitizes arbitrary text input by removing HTML tags, trimming whitespace,
    and bounding maximum string length to prevent memory buffer bloat.
    """
    cleaned = strip_html_tags(text)
    if max_len and len(cleaned) > max_len:
        cleaned = cleaned[:max_len].strip()
    return cleaned
