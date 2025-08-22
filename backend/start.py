#!/usr/bin/env python3
"""
Digital Twin System Backend Startup Script
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import pymysql
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_database():
    """Check if database is accessible"""
    try:
        from app.database import engine
        from sqlalchemy import text  # <-- Add this import
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # <-- Use text() here
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please ensure:")
        print("1. XAMPP is running")
        print("2. MySQL service is started")
        print("3. Database 'digital_twin' exists")
        return False

def initialize_database():
    """Initialize database tables and sample data"""
    try:
        from app.init_db import init
        init()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    try:
        import uvicorn
        print("🚀 Starting Digital Twin System Backend...")
        print("📖 API Documentation will be available at: http://localhost:8000/docs")
        print("🔌 WebSocket endpoint: ws://localhost:8000/ws/{client_type}")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

def main():
    """Main startup function"""
    print("=" * 60)
    print("🔧 Digital Twin System Backend Startup")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("app").exists():
        print("❌ Please run this script from the backend directory")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check database
    if not check_database():
        print("\n💡 To create the database:")
        print("1. Open phpMyAdmin (http://localhost/phpmyadmin)")
        print("2. Create a new database named 'digital_twin'")
        print("3. Run this script again")
        sys.exit(1)
    
    # Initialize database
    print("\n🗄️  Initializing database...")
    if not initialize_database():
        print("⚠️  Database initialization failed, but continuing...")
    
    # Start server
    print("\n" + "=" * 60)
    start_server()

if __name__ == "__main__":
    main() 