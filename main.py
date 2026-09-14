import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from agent import Agent

load_dotenv()

logging.basicConfig(
      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
      level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BOT_NAME = "Ivy Park"

if not TELEGRAM_TOKEN or not GROQ_API_KEY:
      raise ValueError("Missing TELEGRAM_TOKEN or GROQ_API_KEY")

agent = Agent(GROQ_API_KEY, "memory.db", BOT_NAME)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
      await update.message.reply_text(f"👋 Hi! I'm {BOT_NAME}. Send me a message!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
      await update.message.reply_text(f"I'm {BOT_NAME}, your AI assistant. Just send me a message!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
      user_id = update.effective_user.id
      user_message = update.message.text

    logger.info(f"User {user_id}: {user_message}")
    await update.message.chat.send_action("typing")

    try:
              response = agent.process_message(user_id, user_message)
              await update.message.reply_text(response)
              logger.info(f"Response: {response}")
except Exception as e:
          logger.error(f"Error: {str(e)}")
          await update.message.reply_text("Sorry, I encountered an error.")

def main():
      logger.info(f"Starting {BOT_NAME}...")
      application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info(f"✅ {BOT_NAME} is running!")
    application.run_polling()

if __name__ == '__main__':
      main()
