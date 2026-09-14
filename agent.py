import sqlite3
import requests
import logging

logger = logging.getLogger(__name__)

class Agent:
      def __init__(self, api_key: str, db_path: str, bot_name: str = "Ivy Park"):
                self.api_key = api_key
                self.bot_name = bot_name
                self.db_path = db_path
                self.base_url = "https://api.groq.com/openai/v1"
                self.model = "groq/compound"
                self.max_tokens = 500
                self.init_db()

      def init_db(self):
                conn = sqlite3.connect(self.db_path)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        role TEXT,
                        message TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                conn.close()

      def add_message(self, user_id: int, role: str, message: str):
                conn = sqlite3.connect(self.db_path)
                conn.execute("INSERT INTO conversations (user_id, role, message) VALUES (?, ?, ?)",
                             (user_id, role, message))
                conn.commit()
                conn.close()

      def get_history(self, user_id: int) -> str:
                conn = sqlite3.connect(self.db_path)
                rows = conn.execute(
                    "SELECT role, message FROM conversations WHERE user_id = ? ORDER BY timestamp ASC",
                    (user_id,)
                ).fetchall()
                conn.close()

          history = "\n".join([f"{role}: {msg}" for role, msg in rows])
        return history

    def process_message(self, user_id: int, user_message: str) -> str:
              history = self.get_history(user_id)
              self.add_message(user_id, "user", user_message)

        prompt = f"""You are {self.bot_name}, a helpful AI assistant.
        {f'Conversation history:{chr(10)}{history}' if history else ''}

        User: {user_message}
        {self.bot_name}:"""

        try:
                      response = requests.post(
                                        f"{self.base_url}/chat/completions",
                                        headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                                        json={
                                                              "model": self.model,
                                                              "messages": [{"role": "user", "content": prompt}],
                                                              "max_tokens": self.max_tokens,
                                                              "temperature": 0.7
                                        },
                                        timeout=30
                      )

            response.raise_for_status()
            bot_response = response.json()["choices"][0]["message"]["content"].strip()
            self.add_message(user_id, "assistant", bot_response)
            return bot_response

except Exception as e:
            error_msg = f"Error: {str(e)}"
            logger.error(error_msg)
            self.add_message(user_id, "assistant", error_msg)
            return error_msg
