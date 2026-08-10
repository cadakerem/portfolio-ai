# Portfolio AI Lite 📊

An **Open Source Portfolio Manager** built directly on top of Telegram. No complex APIs, no clunky Excel files.
Manage your Stocks and TEFAS Mutual Funds by chatting with your bot and track your live P&L (Profit & Loss) instantly from your phone.

## 🚀 Features
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

---

## ☁️ How to Install & Run 24/7 (For Free)
To keep this bot running 24/7 even when your computer is off, we highly recommend deploying it to **PythonAnywhere** (a completely free cloud server). Unlike Render or Heroku, PythonAnywhere will **never delete your SQLite database (persistent disk).**

### Step 1: Get Your Bot Token
1. Open Telegram and search for `@BotFather`.
2. Type `/newbot` to create a new bot and give it a name.
3. Copy the **HTTP API Token** provided by BotFather.

### Step 2: Upload to PythonAnywhere
1. Go to [PythonAnywhere.com](https://www.pythonanywhere.com/) and create a free Beginner account.
2. Click on the **Files** tab at the top right.
3. Upload all the files from this repository (including the `core` folder).
4. Go to the **Consoles** tab, start a new **Bash** console, and install the requirements:
   `pip install -r requirements.txt`

### Step 3: Run It
1. In the same Bash console, run the following commands:
   `export TELEGRAM_BOT_TOKEN="PASTE_YOUR_TOKEN_HERE"`
   `python main.py`
2. Once you see "Bot is running..." on the screen, you're done!
3. Go to your bot on Telegram and type `/start`.

*Note: Free PythonAnywhere accounts do not support "Always-on tasks", so you may need to keep the bash console running or use the "Tasks" feature to schedule it as a daily cron job.*