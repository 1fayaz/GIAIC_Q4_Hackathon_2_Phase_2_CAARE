#!/usr/bin/env python3
"""
Final verification script to confirm database initialization is working
"""

import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables

from sqlalchemy import create_engine, inspect
from sqlmodel import SQLModel
from src.config.settings import settings
from src.models.user import User  # This will register the model
from src.models.task import Task  # This will register the model

def final_verification():
    print("=== FINAL DATABASE INITIALIZATION VERIFICATION ===")

    # 1. Verify DATABASE_URL is loaded
    print(f"1. DATABASE_URL loaded: {bool(settings.database_url)}")
    if not settings.database_url or settings.database_url == "postgresql://user:password@localhost/dbname":
        print("   [ERROR] DATABASE_URL not properly configured")
        return False

    # 2. Create sync engine
    print("\n2. Creating database engine...")
    sync_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
    engine = create_engine(sync_url, echo=False)
    print("   [SUCCESS] Engine created")

    # 3. Verify models are registered
    print(f"\n3. SQLModel metadata contains {len(SQLModel.metadata.tables)} tables:")
    for table_name in SQLModel.metadata.tables.keys():
        print(f"   - {table_name}")

    # 4. Create tables
    print("\n4. Creating tables...")
    SQLModel.metadata.create_all(engine)
    print("   [SUCCESS] Tables creation attempted")

    # 5. Verify tables exist
    print("\n5. Verifying tables exist...")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"   Tables found: {tables}")

    required_tables = ['user', 'task']
    missing_tables = [table for table in required_tables if table not in tables]

    if missing_tables:
        print(f"   [ERROR] Missing tables: {missing_tables}")
        return False
    else:
        print("   [SUCCESS] All required tables exist")

    # 6. Check user table columns
    if 'user' in tables:
        user_columns = [col['name'] for col in inspector.get_columns('user')]
        required_user_cols = ['id', 'email', 'created_at', 'updated_at']
        missing_user_cols = [col for col in required_user_cols if col not in user_columns]

        if missing_user_cols:
            print(f"   [ERROR] Missing columns in user table: {missing_user_cols}")
            return False
        else:
            print("   [SUCCESS] User table has all required columns")

    # 7. Check task table columns
    if 'task' in tables:
        task_columns = [col['name'] for col in inspector.get_columns('task')]
        required_task_cols = ['id', 'title', 'description', 'completed', 'user_id', 'created_at', 'updated_at']
        missing_task_cols = [col for col in required_task_cols if col not in task_columns]

        if missing_task_cols:
            print(f"   [ERROR] Missing columns in task table: {missing_task_cols}")
            return False
        else:
            print("   [SUCCESS] Task table has all required columns")

    print("\n=== VERIFICATION COMPLETE ===")
    print("[SUCCESS] Database initialization is working correctly!")
    print("All required tables and columns are present in the database.")
    return True

if __name__ == "__main__":
    success = final_verification()
    exit(0 if success else 1)