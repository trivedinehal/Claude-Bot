# Ivy Park Bot - Test Bot

A simple AI bot that runs on Telegram with memory, context, and LLM switching.

## Architecture

```
Telegram Message
    ↓
main.py (listens for messages)
    ↓
agent.py (orchestrates)
    ↓
memory.py (SQLite) + llm.py (Groq)
    ↓
Response back to Telegram
```

## Files

- **main.py** - Telegram listener & entry point
- **agent.py** - Core agent logic
- **memory.py** - SQLite conversation storage
- **llm.py** - Groq API interface
- **.env** - API keys & configuration (don't commit!)
- **requirements.txt** - Python dependencies

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Check .env file
Make sure `.env` has:
- `TELEGRAM_TOKEN` (your bot token)
- `GROQ_API_KEY` (your Groq API key)
- `LLM=groq` (the model to use)

### 3. Run the bot
```bash
python main.py
```

You should see:
```
✅ Ivy Park is running! Send messages to @ivy_park_bot
```

### 4. Test
Open Telegram, find @ivy_park_bot, send a message!

## Commands

```
/start    - Introduction
/help     - Show commands
/status   - Check bot status & conversation length
/clear    - Clear conversation history
```

## How it works

1. **You send message** → Telegram receives it
2. **Bot receives** → Pulls conversation history from SQLite
3. **Bot calls Groq** → Sends context + message to Groq API
4. **Groq responds** → Returns generated response
5. **Bot stores** → Saves user message + response in SQLite
6. **Bot replies** → Sends response back to Telegram

All conversation history is stored locally in `ivy_park_memory.db`

## Memory Structure

```
SQLite Table: messages
├── id (auto-increment)
├── user_id (Telegram user ID)
├── timestamp
├── role (user or assistant)
└── content (the actual message)
```

## To switch LLM later

Edit `.env`:
```
LLM=groq          # Current
LLM=gpt           # Would work with OpenAI key
LLM=claude        # Would work with Anthropic key
```

Then restart the bot.

## Notes

- Bot runs locally (stops when you close terminal)
- To run 24/7, deploy to Railway/Render
- Memory persists in `ivy_park_memory.db`
- Each user gets separate conversation history
- Token limits: Free Groq tier has rate limits
