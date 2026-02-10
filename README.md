# Finance Management System

Shaxsiy moliya va hamyonlarni boshqarish tizimi. Ushbu loyiha yordamida foydalanuvchilar o'z xarajatlari va daromadlarini kuzatib borishlari, bir nechta valyutada hamyonlar ochishlari va batafsil statistika olishlari mumkin.

## 🌟 Asosiy Imkoniyatlar

- **Autentifikatsiya**: Telefon raqami va OTP kod orqali xavfsiz ro'yxatdan o'tish va kirish.
- **Hamyonlar**: Turli xil valyutalarda (UZS, USD, EUR va h.k.) hamyonlar yaratish va boshqarish.
- **Tranzaksiyalar**: Kirim va chiqim operatsiyalarini vaqtini ko'rsatgan holda saqlash.
- **O'tkazmalar**: Hamyonlararo pul o'tkazmalari (valyuta konvertatsiyasi bilan).
- **Statistika**: Kunlik, haftalik, oylik va yillik tahliliy grafiklar va ma'lumotlar.
- **Ko'p tillilik**: O'zbek, Rus va Ingliz tillari qo'llab-quvvatlanadi.
- **Chat tizimi**: Foydalanuvchilar va administratorlar o'rtasida muloqot qilish imkoniyati.

## 🚀 Texnologiyalar

- **Backend**: Django (Python)
- **Ma'lumotlar bazasi**: SQLite (Production uchun PostgreSQL tavsiya etiladi)
- **Frontend**: HTML5, Vanilla CSS, JavaScript (Bootstrap 5)
- **Sozlamalar**: Python-dotenv (.env orqali boshqariladi)

## 🛠 O'rnatish

1. Loyihani yuklab oling:
   ```bash
   git clone <repository_url>
   cd imtihon
   ```

2. Virtual muhitni yarating va faollashtiring:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. Zaruriy kutubxonalarni o'rnating:
   ```bash
   pip install -r requirements.txt
   ```

4. `.env` faylini sozlang (namuna):
   ```ini
   SECRET_KEY=sizing_maxfiy_kalitingiz
   DEBUG=True
   DB_NAME=db.sqlite3
   TIME_ZONE=Asia/Tashkent
   LANGUAGE_CODE=uz
   ```

5. Ma'lumotlar bazasini migratsiya qiling:
   ```bash
   python manage.py migrate
   ```

6. Serverni ishga tushiring:
   ```bash
   python manage.py runserver
   ```

## 📝 Eslatma

Loyiha hozirda ishlab chiqish (Development) bosqichida. Xavfsizlik uchun `DEBUG=False` qilib ishlatish va `SECRET_KEY`ni maxfiy saqlash tavsiya etiladi.
