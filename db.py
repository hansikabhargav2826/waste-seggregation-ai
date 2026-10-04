import sqlite3
import hashlib
from typing import Optional, Dict, Any

DB_PATH = "waste_segregation.db"

# ================= CONNECTION =================
def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ================= INIT DB =================
def init_database() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        eco_score INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        image_name TEXT,
        waste_category TEXT NOT NULL,
        condition TEXT NOT NULL,
        confidence REAL NOT NULL,
        disposal_instruction TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    conn.commit()
    conn.close()

# ================= SECURITY =================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ================= USER =================
def create_user(username: str, password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO users (username, password_hash)
        VALUES (?, ?)
        """, (username, hash_password(password)))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()

# ================= LOGIN =================
def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, username, eco_score
    FROM users
    WHERE username = ? AND password_hash = ?
    """, (username, hash_password(password)))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row["id"],
            "username": row["username"],
            "eco_score": row["eco_score"]
        }

    return None

# ================= SAVE PREDICTION =================
def save_prediction(user_id: int, image_name: str, waste_category: str,
                    condition: str, confidence: float,
                    disposal_instruction: str) -> int:

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions (
        user_id, image_name, waste_category,
        condition, confidence, disposal_instruction
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, image_name, waste_category,
          condition, confidence, disposal_instruction))

    prediction_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return prediction_id

# ================= UPDATE ECO SCORE =================
def update_eco_score(user_id: int, points: int) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET eco_score = eco_score + ?
    WHERE id = ?
    """, (points, user_id))

    cursor.execute("""
    SELECT eco_score FROM users WHERE id = ?
    """, (user_id,))

    new_score = cursor.fetchone()["eco_score"]

    conn.commit()
    conn.close()

    return new_score

