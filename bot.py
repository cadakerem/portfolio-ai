import os
import sqlite3
import telebot
import yfinance as yf

# Bot Token'ı ortam değişkenlerinden veya doğrudan buraya yazarak alıyoruz
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "BURAYA_TOKEN_GELECEK")
bot = telebot.TeleBot(TOKEN)

# Veritabanı Kurulumu (SQLite)
def init_db():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolio (
            user_id INTEGER,
            ticker TEXT,
            amount REAL,
            avg_price REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "📊 *Portfolio AI Lite'a Hoş Geldin!*\n\n"
        "Bu bot ile portföyünüzü kolayca mesaj üzerinden yönetebilirsiniz. "
        "Aşağıdaki komutları kullanın:\n\n"
        "➕ `/ekle <HİSSE> <ADET> <MALİYET>`\n"
        "Örnek: `/ekle AAPL 10 150`\n\n"
        "➖ `/sil <HİSSE>`\n"
        "Örnek: `/sil AAPL`\n\n"
        "💼 `/portfoy`\n"
        "Tüm portföyünüzün kâr/zarar durumunu gösterir."
    )
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['ekle'])
def add_asset(message):
    try:
        parts = message.text.split()
        if len(parts) != 4:
            bot.reply_to(message, "⚠️ Hatalı format. Doğru kullanım: `/ekle THYAO.IS 10 250.5`", parse_mode='Markdown')
            return

        ticker = parts[1].upper()
        amount = float(parts[2])
        avg_price = float(parts[3])
        user_id = message.from_user.id

        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        
        # Eğer zaten varsa güncelle, yoksa ekle
        cursor.execute("SELECT amount, avg_price FROM portfolio WHERE user_id=? AND ticker=?", (user_id, ticker))
        row = cursor.fetchone()
        
        if row:
            # Maliyet ortalaması hesapla
            old_amount, old_price = row
            new_amount = old_amount + amount
            new_avg = ((old_amount * old_price) + (amount * avg_price)) / new_amount
            cursor.execute("UPDATE portfolio SET amount=?, avg_price=? WHERE user_id=? AND ticker=?", 
                           (new_amount, new_avg, user_id, ticker))
        else:
            cursor.execute("INSERT INTO portfolio (user_id, ticker, amount, avg_price) VALUES (?, ?, ?, ?)", 
                           (user_id, ticker, amount, avg_price))
            
        conn.commit()
        conn.close()

        bot.reply_to(message, f"✅ *{ticker}* başarıyla eklendi! Toplam adet: {amount}", parse_mode='Markdown')

    except Exception as e:
        bot.reply_to(message, f"❌ Bir hata oluştu: {str(e)}")

@bot.message_handler(commands=['sil'])
def remove_asset(message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            bot.reply_to(message, "⚠️ Hatalı format. Doğru kullanım: `/sil THYAO.IS`", parse_mode='Markdown')
            return

        ticker = parts[1].upper()
        user_id = message.from_user.id

        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM portfolio WHERE user_id=? AND ticker=?", (user_id, ticker))
        deleted = cursor.rowcount
        conn.commit()
        conn.close()

        if deleted > 0:
            bot.reply_to(message, f"🗑️ *{ticker}* portföyünüzden silindi.", parse_mode='Markdown')
        else:
            bot.reply_to(message, f"⚠️ *{ticker}* portföyünüzde bulunamadı.", parse_mode='Markdown')

    except Exception as e:
        bot.reply_to(message, f"❌ Bir hata oluştu: {str(e)}")

@bot.message_handler(commands=['portfoy'])
def view_portfolio(message):
    user_id = message.from_user.id
    bot.reply_to(message, "⏳ Fiyatlar çekiliyor, lütfen bekleyin...")

    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute("SELECT ticker, amount, avg_price FROM portfolio WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        bot.reply_to(message, "📁 Portföyünüz şu an boş. `/ekle` komutu ile varlık ekleyebilirsiniz.", parse_mode='Markdown')
        return

    total_value = 0
    total_cost = 0
    response = "💼 *PORTFÖY ÖZETİ*\n\n"
    
    # TEFAS Verilerini Toplu Çek (Gerekirse)
    tefas_funds = [r[0] for r in rows if len(r[0]) == 3 and r[0].isalpha()]
    df_tefas = None
    if tefas_funds:
        import pytefas
        from datetime import datetime, timedelta
        crawler = pytefas.Crawler()
        bugun = datetime.now().strftime('%Y-%m-%d')
        bas = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        try:
            df_tefas = crawler.fetch(start=bas, end=bugun)
        except:
            pass

    for row in rows:
        ticker, amount, avg_price = row
        try:
            current_price = None
            
            # TEFAS Fonu Kontrolü
            if len(ticker) == 3 and ticker.isalpha():
                if df_tefas is not None and not df_tefas.empty:
                    fund_data = df_tefas[df_tefas['fund_code'] == ticker]
                    if not fund_data.empty:
                        # En güncel fiyata göre sırala
                        fund_data = fund_data.sort_values('date')
                        current_price = float(fund_data['price'].iloc[-1])
            
            # Eğer TEFAS'ta bulunamadıysa veya hisse ise (Yfinance)
            if current_price is None:
                stock = yf.Ticker(ticker)
                current_price = float(stock.fast_info.last_price)
            
            asset_value = current_price * amount
            asset_cost = avg_price * amount
            profit = asset_value - asset_cost
            profit_pct = (profit / asset_cost) * 100

            total_value += asset_value
            total_cost += asset_cost

            icon = "🟢" if profit >= 0 else "🔴"
            response += f"{icon} *{ticker}*\n"
            response += f"Adet: {amount} | Maliyet: {avg_price:.2f} | Güncel: {current_price:.2f}\n"
            response += f"Değer: {asset_value:.2f} (Kâr: {profit:.2f} | %{profit_pct:.2f})\n\n"
        except Exception as e:
            response += f"⚠️ *{ticker}* fiyatı alınamadı.\n\n"

    total_profit = total_value - total_cost
    total_profit_pct = (total_profit / total_cost) * 100 if total_cost > 0 else 0
    total_icon = "🟩" if total_profit >= 0 else "🟥"

    response += "➖➖➖➖➖➖➖➖\n"
    response += f"💰 *Toplam Yatırım:* {total_cost:.2f}\n"
    response += f"🏦 *Güncel Bakiye:* {total_value:.2f}\n"
    response += f"{total_icon} *Net Durum:* {total_profit:.2f} (%{total_profit_pct:.2f})"

    bot.send_message(message.chat.id, response, parse_mode='Markdown')

if __name__ == '__main__':
    print("Bot çalışıyor...")
    bot.infinity_polling()
