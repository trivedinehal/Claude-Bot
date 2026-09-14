import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from agent import Agent

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize agent
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_PATH = os.getenv("DATABASE_PATH", "ivy_park_memory.db")
BOT_NAME = os.getenv("BOT_NAME", "Ivy Park")

agent = Agent(GROQ_API_KEY, DATABASE_PATH, BOT_NAME)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        f"👋 Hi! I'm {BOT_NAME}. I'm here to help!\n\n"
        "Commands:\n"
        "/status - Check my status\n"
        "/clear - Clear conversation history\n"
        "/help - Show this help"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        f"I'm {BOT_NAME}, your AI assistant.\n\n"
        "Just send me a message and I'll respond!\n\n"
        "Commands:\n"
        "/status - Check status & conversation length\n"
        "/clear - Clear our conversation\n"
        "/help - Show this message"
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    user_id = update.effective_user.id
    status = agent.get_status(user_id)
    await update.message.reply_text(status)

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clear command"""
    user_id = update.effective_user.id
    result = agent.clear_memory(user_id)
    await update.message.reply_text(result)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages"""
    user_id = update.effective_user.id
    user_message = update.message.text

    logger.info(f"User {user_id}: {user_message}")

    # Show typing indicator
    await update.message.chat.send_action("typing")

    # Process message through agent
    response = agent.process_message(user_id, user_message)

    # Send response
    await update.message.reply_text(response)

    logger.info(f"Response: {response}")

def main():
    """Start the bot"""
    logger.info(f"Starting {BOT_NAME}...")

    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("clear", clear_command))

    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    logger.info(f"✅ {BOT_NAME} is running! Send messages to @ivy_park_bot")
    application.run_polling()

if __name__ == '__main__':
    main()
