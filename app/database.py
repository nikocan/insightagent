"""SQLite database helpers supplying connections and schema creation."""

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

DATABASE_PATH = Path(os.getenv("INSIGHTAGENT_DB", "insightagent.db"))


def dict_factory(cursor: sqlite3.Cursor, row: tuple) -> dict:
    """Convert SQLite rows to dictionaries keyed by column names."""

    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def initialize_db() -> None:
    """Create tables if they do not yet exist."""

    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.executescript(
            """
            PRAGMA foreign_keys = ON;
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gtin TEXT,
                upc TEXT,
                brand TEXT NOT NULL,
                title TEXT NOT NULL,
                category TEXT,
                specs_json TEXT
            );
            CREATE TABLE IF NOT EXISTS offers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                channel TEXT NOT NULL,
                seller TEXT NOT NULL,
                price REAL NOT NULL,
                currency TEXT NOT NULL,
                stock INTEGER,
                ship_from TEXT,
                last_seen_at TEXT
            );
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                source TEXT NOT NULL,
                rating REAL NOT NULL,
                text TEXT NOT NULL,
                lang TEXT NOT NULL,
                date TEXT,
                sentiment TEXT,
                topics TEXT
            );
            CREATE TABLE IF NOT EXISTS keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                term TEXT NOT NULL,
                intent TEXT,
                volume INTEGER,
                difficulty REAL,
                cpc_est REAL
            );
            CREATE TABLE IF NOT EXISTS insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER UNIQUE NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                sales_score REAL,
                trend_score REAL,
                price_elasticity REAL,
                swot_json TEXT
            );
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                country TEXT,
                moq INTEGER,
                lead_time INTEGER,
                contact TEXT
            );
            CREATE TABLE IF NOT EXISTS product_suppliers (
                product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                supplier_id INTEGER NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
                PRIMARY KEY (product_id, supplier_id)
            );
            CREATE TABLE IF NOT EXISTS rfqs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                supplier_id INTEGER NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
                status TEXT NOT NULL,
                quotes TEXT
            );
            CREATE TABLE IF NOT EXISTS creatives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                copy TEXT NOT NULL,
                assets TEXT
            );
            CREATE TABLE IF NOT EXISTS creative_sizes (
                creative_id INTEGER NOT NULL REFERENCES creatives(id) ON DELETE CASCADE,
                size TEXT NOT NULL,
                PRIMARY KEY (creative_id, size)
            );
            CREATE TABLE IF NOT EXISTS creative_channels (
                creative_id INTEGER NOT NULL REFERENCES creatives(id) ON DELETE CASCADE,
                channel TEXT NOT NULL,
                PRIMARY KEY (creative_id, channel)
            );
            CREATE TABLE IF NOT EXISTS creative_briefs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                tone TEXT,
                objective TEXT,
                primary_message TEXT,
                call_to_action TEXT,
                persona TEXT,
                recommended_channels TEXT
            );
            CREATE TABLE IF NOT EXISTS compliance_guidelines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                level TEXT NOT NULL,
                flagged_claims TEXT,
                guidance TEXT
            );
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                pdf_url TEXT NOT NULL,
                created_by TEXT NOT NULL
            );
            """
        )


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Yield a SQLite connection configured for dict rows."""

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = dict_factory
    try:
        yield conn
    finally:
        conn.close()
