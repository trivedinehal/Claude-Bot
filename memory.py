import sqlite3
from datetime import datetime
from typing import List, Dict

class AvaMemory:
    def __init__(self, db_path: str = "ivy_park_memory.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize the database with messages table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                role TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def add_message(self, user_id: int, role: str, content: str):
        """Add a message to the conversation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)',
            (user_id, role, content)
        )

        conn.commit()
        conn.close()

    def get_conversation(self, user_id: int) -> str:
        """Get formatted conversation history for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            'SELECT role, content FROM messages WHERE user_id = ? ORDER BY timestamp ASC',
            (user_id,)
        )

        messages = cursor.fetchall()
        conn.close()

        if not messages:
            return ""

        # Format as conversation
        formatted = []
        for role, content in messages:
            if role == "user":
                formatted.append(f"You: {content}")
            else:
                formatted.append(f"Ivy Park: {content}")

        return "\n".join(formatted)

    def clear_conversation(self, user_id: int):
        """Clear conversation history for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM messages WHERE user_id = ?', (user_id,))

        conn.commit()
        conn.close()
