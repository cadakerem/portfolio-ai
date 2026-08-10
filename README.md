# Portfolio AI Lite 📊

Bu proje, karmaşık API'lere veya hantal Excel dosyalarına ihtiyaç duymadan, doğrudan Telegram üzerinden çalışan **Açık Kaynaklı bir Portföy Yöneticisidir**. 
Yatırım yaptığınız Hisse Senetlerini ve TEFAS Yatırım Fonlarını mesajlaşarak ekleyebilir, güncel Kâr/Zarar durumunuzu anlık olarak cebinizden takip edebilirsiniz.

## 🚀 Özellikler
- **TEFAS Fonları (`pytefas`):** YAY, MAC, TI3 gibi 3 harfli fon kodlarını otomatik tanır ve güncel fiyatını çeker.
- **Hisse Senetleri (`yfinance`):** AAPL, TSLA, THYAO.IS gibi kodları otomatik tanır ve anlık fiyatını getirir.
- **SQLite Veritabanı:** Kurulum gerektirmeyen, hafif yerel veritabanı.
- **Ortalama Maliyet:** Aynı hisseden farklı fiyata tekrar alım yaptığınızda maliyetinizi otomatik düşürür/yükseltir (Weighted Average).

## 🛠️ Komutlar
Botu başlattıktan sonra şu komutları kullanabilirsiniz:
- `/ekle THYAO.IS 10 250` (10 adet THYAO hissesini 250 TL maliyetle ekler)
- `/ekle MAC 5000 0.12` (5000 pay MAC fonunu 0.12 kuruş maliyetle ekler)
- `/sil THYAO.IS` (Varlığı portföyden siler)
- `/portfoy` (Güncel piyasa verilerini çekerek Kâr/Zarar durumunu listeler)

---

## ☁️ Nasıl Kurulur ve 7/24 Çalıştırılır? (Ücretsiz)
Bu botu bilgisayarınız kapalıyken bile 7/24 çalışması için **PythonAnywhere** adlı tamamen ücretsiz bulut sunucusuna kurmanızı tavsiye ederiz. Render veya Heroku'nun aksine PythonAnywhere SQLite veritabanınızı **asla silmez (kalıcı disk).**

### Adım 1: Bot Token'ı Alma
1. Telegram'a girin ve `@BotFather` ı bulun.
2. `/newbot` yazarak botunuza bir isim ve kullanıcı adı verin.
3. Size verdiği **HTTP API Token**'ı kopyalayın.

### Adım 2: PythonAnywhere'e Yükleme
1. [PythonAnywhere.com](https://www.pythonanywhere.com/)'a girip ücretsiz (Beginner) hesap açın.
2. Sağ üstten **Files** sekmesine tıklayın.
3. Bu projedeki `bot.py` ve `requirements.txt` dosyalarını yükleyin (Upload).
4. **Consoles** sekmesine gidip bir **Bash** konsolu açın ve şunu yazarak kütüphaneleri kurun:
   `pip install -r requirements.txt`

### Adım 3: Çalıştırma
1. Yine Bash konsoluna şunu yazarak botunuzu başlatın:
   `export TELEGRAM_BOT_TOKEN="BURAYA_TOKEN_YAPISTIRIN"`
   `python bot.py`
2. Ekranda "Bot çalışıyor..." yazısını gördüğünüzde işlem tamamdır! 
3. Kendi botunuza gidip `/start` diyebilirsiniz.

*Not: PythonAnywhere ücretsiz hesaplarında kodun 7/24 aralıksız çalışması için "Always-on tasks" özelliği yoktur, bu nedenle bash sekmesinin açık kalması gerekebilir. Sadece günde 1 kez rapor almak isterseniz "Tasks" bölümünden günlük zamanlayıcı (Cron job) da kurabilirsiniz.*