@echo off
echo ============================================
echo  🐧 Setting up Flask App inside WSL
echo ============================================

:: Check if WSL is installed
where wsl >nul 2>&1
IF ERRORLEVEL 1 (
    echo WSL is not installed. Installing WSL...
    wsl --install
    echo Please restart your system to complete the WSL installation.
    pause
    exit /b
) ELSE (
    echo ✅ WSL is installed.
)

:: Launch WSL and run all setup commands inside it
echo --------------------------------------------
echo 🚀 Launching WSL and configuring environment...
echo --------------------------------------------

wsl bash -c "
echo ============================================
echo 📦 Setting up Python virtual environment...
python3 -m venv webenv && \
source webenv/bin/activate && \

echo ✅ Virtual environment 'webenv' activated.
echo --------------------------------------------
echo 📦 Installing dependencies...
pip install --upgrade pip && \
pip install -r requirements.txt && \

echo ✅ Dependencies installed.
echo --------------------------------------------
echo 🌱 Running seed.py to populate the database...
export FLASK_APP=app.py && \
python3 seed.py && \

echo ✅ Database seeded.
echo --------------------------------------------
echo 🚀 Launching the Flask app...
python3 app.py
"

:: Open browser
echo --------------------------------------------
echo 🌐 Opening your app in the default browser...
start http://localhost:5000

echo ============================================
echo ✅ Flask app is running in WSL 🎉
echo ============================================

pause
