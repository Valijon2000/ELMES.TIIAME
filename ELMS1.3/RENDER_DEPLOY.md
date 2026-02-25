# Render serverga ELMS joylash

Repozitoriya: **https://github.com/Valijon2000/ELMES.TIIAME**

## 1. GitHub ga yuklash

- **GitHub Desktop** yoki **CMD** da loyiha papkasiga o‘ting: `c:\Users\User\Desktop\LMS\ELMS1.3\ELMS1.3`
- `github_yuklash.bat` ni ishga tushiring yoki:
  ```bash
  git init
  git add .
  git commit -m "ELMS - Render uchun"
  git remote add origin https://github.com/Valijon2000/ELMES.TIIAME.git
  git branch -M main
  git push -u origin main
  ```

## 2. Render da yangi Web Service

1. [render.com](https://render.com) → **Dashboard** → **New** → **Web Service**
2. **Connect repository** → GitHub bilan ulang → **Valijon2000/ELMES.TIIAME** ni tanlang
3. Sozlamalar (avtomatik bo‘lishi mumkin):
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn run:app --bind 0.0.0.0:$PORT`
4. **Environment** da:
   - **SECRET_KEY** — Render yoki siz yaratgan maxfiy kalit
   - **DATABASE_URL** — (ixtiyoriy) Agar Render PostgreSQL qo‘shsangiz, avtomatik beriladi
5. **Create Web Service** → deploy tugayguncha kuting.

## 3. Muhim

- Birinchi marta **SQLite** ishlatiladi (ma’lumotlar server qayta ishga tushganda yangilanadi).
- Doimiy ma’lumot uchun Render **PostgreSQL** qo‘shing va **DATABASE_URL** ni o‘rnating.
- **config.py** allaqachon `DATABASE_URL` ni o‘qiydi; PostgreSQL uchun `sqlite:///` o‘rniga `postgresql://` ishlatiladi.
