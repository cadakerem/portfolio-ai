import telebot
import time
import threading
from datetime import datetime
from core.config import TOKEN
from core.database import init_db, add_or_update_asset, remove_asset, get_portfolio, get_all_users, set_user_schedule, get_users_by_time
from core.finance import fetch_tefas_funds, get_current_price

bot = telebot.TeleBot(TOKEN)
init_db()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "📊 *Welcome to Portfolio AI Lite!*\n\n"
        "Manage your portfolio easily via text messages. "
        "Use the following commands:\n\n"
        "➕ `/add <TICKER> <AMOUNT> <COST>`\n"
        "Example: `/add AAPL 10 150`\n\n"
        "➖ `/remove <TICKER>`\n"
        "Example: `/remove AAPL`\n\n"
        "💼 `/portfolio`\n"
        "Shows your overall portfolio P&L.\n\n"
        "⏰ `/settime <MORNING> <EVENING>`\n"
        "Example: `/settime 10:15 17:45`"
    )
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['add'])
def add_command(message):
    try:
        parts = message.text.split()
        if len(parts) != 4:
            bot.reply_to(message, "⚠️ Invalid format. Usage: `/add THYAO.IS 10 250.5`", parse_mode='Markdown')
            return

        ticker = parts[1].upper()
        amount = float(parts[2])
        avg_price = float(parts[3])
        user_id = message.from_user.id

        add_or_update_asset(user_id, ticker, amount, avg_price)
        bot.reply_to(message, f"✅ *{ticker}* added successfully! Total amount: {amount}", parse_mode='Markdown')

    except Exception as e:
        bot.reply_to(message, f"❌ An error occurred: {str(e)}")

@bot.message_handler(commands=['remove'])
def remove_command(message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            bot.reply_to(message, "⚠️ Invalid format. Usage: `/remove THYAO.IS`", parse_mode='Markdown')
            return

        ticker = parts[1].upper()
        user_id = message.from_user.id

        if remove_asset(user_id, ticker):
            bot.reply_to(message, f"🗑️ *{ticker}* removed from your portfolio.", parse_mode='Markdown')
        else:
            bot.reply_to(message, f"⚠️ *{ticker}* not found in your portfolio.", parse_mode='Markdown')

    except Exception as e:
        bot.reply_to(message, f"❌ An error occurred: {str(e)}")

def generate_portfolio_report(user_id):
    rows = get_portfolio(user_id)
    if not rows:
        return "📁 Your portfolio is currently empty. Use `/add` to add assets."

    # Fetch TEFAS funds in bulk if needed
    tefas_funds = [r[0] for r in rows if len(r[0]) == 3 and r[0].isalpha()]
    df_tefas = fetch_tefas_funds() if tefas_funds else None

    total_value = 0
    total_cost = 0
    response = "💼 *PORTFOLIO SUMMARY*\n\n"

    for row in rows:
        ticker, amount, avg_price = row
        try:
            current_price = get_current_price(ticker, df_tefas)
            
            asset_value = current_price * amount
            asset_cost = avg_price * amount
            profit = asset_value - asset_cost
            profit_pct = (profit / asset_cost) * 100

            total_value += asset_value
            total_cost += asset_cost

            icon = "🟢" if profit >= 0 else "🔴"
            response += f"{icon} *{ticker}*\n"
            response += f"Amount: {amount} | Cost: {avg_price:.2f} | Current: {current_price:.2f}\n"
            response += f"Value: {asset_value:.2f} (P&L: {profit:.2f} | {profit_pct:.2f}%)\n\n"
        except Exception as e:
            response += f"⚠️ Failed to fetch price for *{ticker}*.\n\n"

    total_profit = total_value - total_cost
    total_profit_pct = (total_profit / total_cost) * 100 if total_cost > 0 else 0
    total_icon = "🟩" if total_profit >= 0 else "🟥"

    response += "➖➖➖➖➖➖➖➖\n"
    response += f"💰 *Total Invested:* {total_cost:.2f}\n"
    response += f"🏦 *Current Value:* {total_value:.2f}\n"
    response += f"{total_icon} *Net P&L:* {total_profit:.2f} ({total_profit_pct:.2f}%)"
    return response


@bot.message_handler(commands=['portfolio'])
def view_portfolio_command(message):
    user_id = message.from_user.id
    bot.reply_to(message, "⏳ Fetching live prices, please wait...")
    report = generate_portfolio_report(user_id)
    bot.send_message(message.chat.id, report, parse_mode='Markdown')

@bot.message_handler(commands=['settime'])
def set_time_command(message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            bot.reply_to(message, "⚠️ Invalid format. Usage: `/settime 10:15 17:45`", parse_mode='Markdown')
            return

        morning_time = parts[1]
        evening_time = parts[2]
        user_id = message.from_user.id
        
        # Basic validation
        if len(morning_time) != 5 or len(evening_time) != 5 or ":" not in morning_time or ":" not in evening_time:
            bot.reply_to(message, "⚠️ Invalid time format. Please use HH:MM format like `10:15`.", parse_mode='Markdown')
            return

        set_user_schedule(user_id, morning_time, evening_time)
        bot.reply_to(message, f"⏰ Schedule updated! You will receive daily reports at {morning_time} and {evening_time}.", parse_mode='Markdown')

    except Exception as e:
        bot.reply_to(message, f"❌ An error occurred: {str(e)}")

def send_scheduled_reports():
    now = datetime.now().strftime("%H:%M")
    users = get_users_by_time(now)
    for user_id in users:
        try:
            report = generate_portfolio_report(user_id)
            if "📁 Your portfolio is currently empty" not in report:
                bot.send_message(user_id, f"🌅 *Daily Automatic Report*\n\n{report}", parse_mode='Markdown')
        except Exception as e:
            print(f"Failed to send report to {user_id}: {e}")

def schedule_checker():
    while True:
        # Check at the start of every minute
        now = datetime.now()
        if now.second == 0:
            send_scheduled_reports()
            time.sleep(60) # Sleep for a minute after sending
        else:
            time.sleep(1)

if __name__ == '__main__':
    print("Starting dynamic scheduler...")
    threading.Thread(target=schedule_checker, daemon=True).start()
    
    print("Bot is running...")
    bot.infinity_polling()
