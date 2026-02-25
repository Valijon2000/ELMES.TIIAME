@echo off
chcp 65001 >nul
echo ========================================
echo   Line endings (CRLF/LF) ni tuzatish
echo ========================================
echo.

cd /d "%~dp0"

where git >nul 2>&1
if errorlevel 1 (
    echo [XATO] Git topilmadi. GitHub Desktop yoki Git CLI o'rnating.
    pause
    exit /b 1
)

echo 1. Git sozlash: core.autocrlf=true (Windows)
git config --global core.autocrlf true
echo.

echo 2. Staging ni tozalash...
git reset HEAD
echo.

echo 3. .gitattributes mavjud - line ending qoidalari qo'llanadi.
echo.

echo 4. Fayllarni qayta normalizatsiya qilish (--renormalize)...
git add --renormalize .
git add .
echo.

echo 5. O'zgarishlarni commit qilish...
git diff --cached --quiet 2>nul
if errorlevel 1 (
    git commit -m "Fix line endings (normalize to LF)"
    echo Commit qilindi.
) else (
    echo O'zgarishlar yo'q yoki allaqachon normal.
)
echo.

echo 6. GitHub ga yuborish...
git remote remove origin 2>nul
git remote add origin https://github.com/Valijon2000/ELMES.TIIAME.git
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo Push xato. GitHub login/token tekshiring.
) else (
    echo.
    echo [OK] Line endings tuzatildi va yuklandi: https://github.com/Valijon2000/ELMES.TIIAME
)

echo.
pause
