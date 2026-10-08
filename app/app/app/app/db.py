import sqlite3
from pathlib import Path
from .config import DB_PATH

def connect():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as c:
        c.executescript('''
        CREATE TABLE IF NOT EXISTS players (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            name TEXT NOT NULL,
            coins INTEGER NOT NULL DEFAULT 100,
            gems INTEGER NOT NULL DEFAULT 0,
            tickets INTEGER NOT NULL DEFAULT 0,
            xp INTEGER NOT NULL DEFAULT 0,
            level INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS mochi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            species TEXT NOT NULL,
            rarity TEXT NOT NULL,
            level INTEGER NOT NULL DEFAULT 1,
            power INTEGER NOT NULL DEFAULT 10,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        ''')

def ensure_player(user_id, username, name):
    with connect() as c:
        c.execute('''
        INSERT INTO players(user_id, username, name)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username=excluded.username, name=excluded.name
        ''', (user_id, username, name))

def get_player(user_id):
    with connect() as c:
        return c.execute("SELECT * FROM players WHERE user_id=?", (user_id,)).fetchone()

def add_currency(user_id, coins=0, gems=0, tickets=0):
    with connect() as c:
        c.execute(
            "UPDATE players SET coins=coins+?, gems=gems+?, tickets=tickets+? WHERE user_id=?",
            (coins, gems, tickets, user_id)
        )

def add_xp(user_id, amount):
    with connect() as c:
        p = c.execute("SELECT xp, level FROM players WHERE user_id=?", (user_id,)).fetchone()
        if not p:
            return
        xp = p["xp"] + amount
        level = p["level"]
        while xp >= level * 100:
            xp -= level * 100
            level += 1
        c.execute("UPDATE players SET xp=?, level=? WHERE user_id=?", (xp, level, user_id))

def add_mochi(user_id, species, rarity, power):
    with connect() as c:
        c.execute(
            "INSERT INTO mochi(user_id,species,rarity,power) VALUES(?,?,?,?)",
            (user_id, species, rarity, power)
        )

def get_mochi(user_id):
    with connect() as c:
        return c.execute(
            "SELECT * FROM mochi WHERE user_id=? ORDER BY id DESC", (user_id,)
        ).fetchall()

def leaderboard(limit=10):
    with connect() as c:
        return c.execute(
            "SELECT name, level, xp, coins FROM players ORDER BY level DESC, xp DESC LIMIT ?",
            (limit,)
        ).fetchall()
