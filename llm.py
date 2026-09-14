from groq import Groq
import os

class LLMInterface:
    def __init__(self, api_key: str, model: str = "mixtral-8x7b-32768"):
        self.api_key = api_key
        self.model = model
        self.client = Groq(api_key=api_key)

    def generate_response(self, conversation_history: str, user_message: str, bot_name: str = "Ivy Park") -> str:
        """
        Generate a response from Groq based on conversation history and new message

        Args:
            conversation_history: Full formatted conversation history
            user_message: The new user message
            bot_name: Name of the bot (for context)

        Returns:
            Generated response from Groq
        """

        # Build the prompt
        if conversation_history:
            prompt = f"""You are {bot_name}, a helpful AI assistant. Here's the conversation history:

{conversation_history}

User: {user_message}

{bot_name}: """
        else:
            prompt = f"""You are {bot_name}, a helpful AI assistant.

User: {user_message}

{bot_name}: """

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            response = message.content[0].text
            return response.strip()

        except Exception as e:
            return f"Error generating response: {str(e)}"

    def set_model(self, model: str):
        """Switch to a different model"""
        self.model = model
