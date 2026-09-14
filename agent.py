from memory import AvaMemory
from llm import LLMInterface

class Agent:
    def __init__(self, groq_api_key: str, db_path: str, bot_name: str = "Ivy Park"):
        self.memory = AvaMemory(db_path)
        self.llm = LLMInterface(groq_api_key)
        self.bot_name = bot_name

    def process_message(self, user_id: int, user_message: str) -> str:
        """
        Process a user message and generate a response

        Flow:
        1. Get conversation history from memory
        2. Call LLM with context
        3. Store user message in memory
        4. Store response in memory
        5. Return response
        """

        # Step 1: Get conversation history
        conversation_history = self.memory.get_conversation(user_id)

        # Step 2: Generate response using LLM
        response = self.llm.generate_response(
            conversation_history=conversation_history,
            user_message=user_message,
            bot_name=self.bot_name
        )

        # Step 3: Store user message
        self.memory.add_message(user_id, "user", user_message)

        # Step 4: Store bot response
        self.memory.add_message(user_id, "assistant", response)

        # Step 5: Return response
        return response

    def switch_llm(self, model: str):
        """Switch to a different LLM model"""
        self.llm.set_model(model)
        return f"Switched to {model}"

    def clear_memory(self, user_id: int):
        """Clear conversation history for a user"""
        self.memory.clear_conversation(user_id)
        return "Conversation cleared"

    def get_status(self, user_id: int) -> str:
        """Get status info"""
        history = self.memory.get_conversation(user_id)
        message_count = history.count("\n") // 2 if history else 0
        return f"Status: {self.bot_name} active | Model: {self.llm.model} | Messages: {message_count}"
