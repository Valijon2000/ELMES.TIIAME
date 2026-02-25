# Loyihani GitHub ga joylash (https://github.com/valijon0119/elm.git)

## 1. Git o‘rnatish (agar yo‘q bo‘lsa)

- [Git for Windows](https://git-scm.com/download/win) yuklab oling va o‘rnating.
- O‘rnatgach, **CMD** yoki **PowerShell** ni qayta oching.

## 2. Loyiha papkasida terminal ochish

```powershell
cd "c:\Users\User\Desktop\LMS\ELMS1.3"
```

**Muhim:** Loyiha kodi `ELMS1.3` ichidagi `ELMS1.3` papkasida bo‘lsa, avval shu ichki papkaga o‘ting:

```powershell
cd "c:\Users\User\Desktop\LMS\ELMS1.3\ELMS1.3"
```

## 3. Git repozitoriyani boshlash (birinchi marta)

Agar loyihada `.git` papkasi yo‘q bo‘lsa:

```bash
git init
git add .
git commit -m "ELMS loyihasi - boshlang'ich commit"
```

## 4. GitHub repozitoriyasini ulash

```bash
git remote add origin https://github.com/valijon0119/elm.git
```

Agar `origin` allaqachon boshqa manzilga ulangan bo‘lsa:

```bash
git remote set-url origin https://github.com/valijon0119/elm.git
```

## 5. Asosiy branch nomi va push

```bash
git branch -M main
git push -u origin main
```

GitHub’da login/parol yoki **Personal Access Token** so‘raladi. Token yaratish: GitHub → Settings → Developer settings → Personal access tokens.

---

## Qisqa variant (Git allaqachon o‘rnatilgan bo‘lsa)

Loyiha **ichki** `ELMS1.3` papkasida bo‘lsa:

```powershell
cd "c:\Users\User\Desktop\LMS\ELMS1.3\ELMS1.3"
git init
git add .
git commit -m "ELMS 1.3 - boshlang'ich"
git remote add origin https://github.com/valijon0119/elm.git
git branch -M main
git push -u origin main
```

Loyiha **tashqi** `ELMS1.3` (ichida .cursor, ELMS1.3, .gitignore bor) da bo‘lsa:

```powershell
cd "c:\Users\User\Desktop\LMS\ELMS1.3"
git init
git add .
git commit -m "ELMS 1.3 - boshlang'ich"
git remote add origin https://github.com/valijon0119/elm.git
git branch -M main
git push -u origin main
```

---

## Keyingi o‘zgarishlarni yuklash

Kod o‘zgargandan keyin:

```bash
git add .
git commit -m "O'zgarishlar tavsifi"
git push
```
