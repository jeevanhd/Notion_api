#!/usr/bin/env python3
"""
Setup script for Notion Integration API
Helps users quickly configure their environment
"""

import os
import sys
import shutil
from pathlib import Path

def main():
    print("🚀 Notion Integration API Setup")
    print("=" * 40)
    
    # Check if .env exists
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists():
        if env_example.exists():
            print("📋 Creating .env file from template...")
            shutil.copy('.env.example', '.env')
            print("✅ .env file created!")
            print("\n📝 Please edit .env file with your actual Notion credentials:")
            print("   - NOTION_TOKEN: Get from https://www.notion.so/my-integrations")
            print("   - DATABASE_ID: Get from your Notion database URL")
        else:
            print("❌ .env.example not found!")
            return False
    else:
        print("✅ .env file already exists")
    
    # Check if requirements are installed
    print("\n📦 Checking dependencies...")
    try:
        import fastapi
        import uvicorn
        import requests
        import pydantic
        from dotenv import load_dotenv
        print("✅ All dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e.name}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    
    # Check environment variables
    print("\n🔍 Checking environment configuration...")
    from dotenv import load_dotenv
    load_dotenv()
    
    notion_token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv('DATABASE_ID')
    
    if not notion_token or notion_token == 'your_notion_integration_token_here':
        print("⚠️  NOTION_TOKEN not configured in .env")
    else:
        print("✅ NOTION_TOKEN configured")
    
    if not database_id or database_id == 'your_notion_database_id_here':
        print("⚠️  DATABASE_ID not configured in .env")
    else:
        print("✅ DATABASE_ID configured")
    
    print("\n🎯 Setup complete!")
    print("\n📚 Next steps:")
    print("1. Edit .env with your actual Notion credentials")
    print("2. Run: python -m uvicorn notion_api:app --reload")
    print("3. Visit: http://localhost:8000/docs")
    print("\n💡 CLI usage: python notion_service.py \"Title\" \"Content\"")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)