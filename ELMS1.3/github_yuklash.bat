@echo off
chcp 65001 >nul
echo ========================================
echo   GitHub ga yuklash (valijon0119/elm)
echo ========================================
echo.

cd /d "%~dp0"

where git >nul 2>&1
if errorlevel 1 (
    echo [XATO] Git topilmadi. Iltimos, Git o'rnating: https://git-scm.com/download/win
    pause
    exit /b 1
)

if not exist ".git" (
    echo Git repozitoriyasi yaratilmoqda...
    git init
    git branch -M main
)

git remote remove origin 2>nul
git remote add origin https://github.com/valijon0119/elm.git

git add .
git diff --cached --quiet 2>nul
if errorlevel 1 git commit -m "ELMS 1.3 - yangilanish"

echo.
echo GitHub ga yuborilmoqda (login/token so'raladi)...
git push -u origin main

if errorlevel 1 (
    echo.
    echo Agar xato bo'lsa: GitHub da Personal Access Token yarating va parol o'rniga token kiriting.
    echo https://github.com/settings/tokens
) else (
    echo.
    echo [OK] Muvaffaqiyatli yuklandi: https://github.com/valijon0119/elm
)

echo.
pause
