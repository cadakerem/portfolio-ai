# 📈 Portfolio AI (Telegram Finance Bot)

A Python-based financial data engine for tracking personal assets. It utilizes yfinance and pytefas for market intelligence, featuring a headless Telegram UI and dynamic background scheduling.

## 🚀 Features
- **AI Portfolio Analysis (Optional):** Integrates dynamically with Groq, OpenAI (ChatGPT), Anthropic (Claude), and Google Gemini to give you a smart financial insight at the end of your reports. We recommend Groq because it is completely free and fast, but you can plug in OpenAI, Claude, or Gemini for deeper analysis!
- **TEFAS Mutual Funds (`pytefas`):** Automatically recognizes 3-letter fund codes (e.g., YAY, MAC, TI3) and fetches the latest prices.
- **Global & Local Stocks (`yfinance`):** Automatically recognizes stock tickers (e.g., AAPL, TSLA, THYAO.IS) and fetches real-time prices.
- **Automated Daily Reports:** Sends you a complete portfolio summary every morning and evening automatically (default is 10:15 and 17:45, but customizable).
- **SQLite Database:** Lightweight local database, zero setup required.
- **Weighted Average Cost:** Automatically calculates your new average cost if you buy the same asset multiple times at different prices.
- **Modular Architecture:** Clean code structure divided into core logic for easy contributions.

## 🛠️ Commands
Once the bot is running, use the following commands:
- `/add THYAO.IS 10 250` (Adds 10 shares of THYAO at 250 TL cost)
- `/add MAC 5000 0.12` (Adds 5000 shares of MAC fund at 0.12 TL cost)
- `/remove THYAO.IS` (Removes the asset from your portfolio)
- `/portfolio` (Fetches live market data and lists your current P&L)
- `/settime 09:30 18:00` (Sets your personal daily report schedule to 09:30 and 18:00)

## 🔒 Privacy & Access Control
- **AI Privacy Note:** If you configure an AI API key (Groq/OpenAI/Claude/Gemini), your portfolio data (tickers, amounts, and prices) will be sent to that provider to generate the insight. If you leave the API key blank, no data leaves your server.
- **Access Control (Private Mode):** By default, anyone who finds your bot can use it. To restrict it to just yourself:
  1. Open Telegram and message `@userinfobot` to get your numeric **User ID** (e.g. `123456789`).
  2. Open the `.env` file and set `ALLOWED_USER_IDS=123456789` (you can separate multiple IDs with commas).
  3. Now, the bot will completely ignore commands from any unauthorized strangers!

## 🧠 Customizing AI Personality
Want the AI to talk like a Wall Street broker, a cautious advisor, or maybe even Yoda? You can easily change its system prompt!
1. Open the file `core/ai.py`
2. Find line 16: `system_prompt = "Sen çok tecrübeli ve profesyonel bir portföy yöneticisisin..."`
3. Change this text to give your AI whatever personality or instruction set you prefer.

---

## 🔑 Setup Step 1: Get Your Private Bot Token
Before installing the bot anywhere, you need to create your own Telegram Bot so it runs privately just for you.
1. Open Telegram and search for `@BotFather`.
2. Send `/newbot` and follow the instructions to create your bot.
3. BotFather will give you a **HTTP API Token** (e.g. `12345:ABCDE`). Copy it.

---

## 💻 Setup Step 2: Choose Your Deployment

### Option A: Local Installation (For Developers)
Want to run the bot on your own computer instead of the cloud?
1. Clone the repository: `git clone https://github.com/cadakerem/portfolio-ai.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your keys (including your Telegram Token).
4. Run the bot: `python main.py`

### Option B: Cloud Server (PythonAnywhere)
To keep this bot running without keeping your computer on, we recommend deploying it to **PythonAnywhere**. Unlike Render or Heroku, PythonAnywhere provides a persistent disk, meaning your SQLite database will never be deleted. 

*Note: PythonAnywhere's free tier requires you to occasionally restart the script. For true 24/7 uninterrupted uptime, a $5/month "Hacker" plan or running it on a local Raspberry Pi/VPS is required.*

1. Go to [PythonAnywhere.com](https://www.pythonanywhere.com/) and create a free Beginner account.
2. Click on the **Files** tab at the top right.
3. Upload all the files from this repository (including the `core` folder).
4. Go to the **Consoles** tab, start a new **Bash** console, and install the requirements:
   `pip install -r requirements.txt`
5. In the same Bash console, run the following commands to start the bot. You only need the Telegram token to start, but you can optionally add one AI API key of your choice to enable smart insights:

```bash
# 1. Export your Telegram Token (Required)
export TELEGRAM_BOT_TOKEN="PASTE_YOUR_TOKEN_HERE"

# 2. Export ONE of the following AI API Keys (Optional)
export GROQ_API_KEY="OPTIONAL_GROQ_KEY_HERE"
# export OPENAI_API_KEY="OPTIONAL_OPENAI_KEY_HERE"
# export ANTHROPIC_API_KEY="OPTIONAL_ANTHROPIC_KEY_HERE"
# export GEMINI_API_KEY="OPTIONAL_GEMINI_KEY_HERE"

# 3. Start the bot
python main.py
```

6. Once you see "Bot is running..." on the screen, you're done! Go to your bot on Telegram and type `/start`.