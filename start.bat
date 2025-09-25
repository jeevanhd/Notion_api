@echo off
echo 🚀 Notion Integration API - Quick Start
echo ========================================

echo 📦 Installing dependencies...
pip install -r requirements.txt

echo.
echo 📋 Setting up environment file...
if not exist .env (
    if exist .env.example (
        copy .env.example .env
        echo ✅ Created .env from template
        echo.
        echo ⚠️  IMPORTANT: Edit .env with your actual Notion credentials:
        echo    - NOTION_TOKEN: Get from https://www.notion.so/my-integrations
        echo    - DATABASE_ID: Get from your Notion database URL
        echo.
        pause
    ) else (
        echo ❌ .env.example not found!
        pause
        exit /b 1
    )
) else (
    echo ✅ .env file already exists
)

echo.
echo 🚀 Starting FastAPI server...
echo Visit: http://localhost:8000/docs for API documentation
echo Press Ctrl+C to stop the server
echo.
python -m uvicorn notion_api:app --reload