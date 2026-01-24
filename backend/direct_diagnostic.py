#!/usr/bin/env python3
"""
Direct diagnostic test to verify database connectivity without problematic imports
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from sqlalchemy import create_engine, inspect, text
from sqlmodel import SQLModel
from src.config.settings import settings

def direct_diagnostic_test():
    print("=== DIRECT DATABASE DIAGNOSTIC TEST ===")

    # Step 1: Check if DATABASE_URL is present
    print(f"1. DATABASE_URL present: {bool(settings.database_url)}")
    if not settings.database_url or settings.database_url == "postgresql://user:password@localhost/dbname":
        print("   [ERROR] DATABASE_URL is not properly configured. Please check your .env file.")
        return False

    print(f"   Database URL scheme: {settings.database_url.split('://')[0]}")

    # Convert to sync URL for testing
    sync_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
    sync_url = sync_url.replace("postgresql+psycopg://", "postgresql://")

    print(f"   Sync URL: {'*' * len(sync_url)}")

    try:
        # Step 2: Create a sync engine for table creation
        print("\n2. Creating sync engine for table operations...")
        engine = create_engine(sync_url, echo=True)
        print("   [SUCCESS] Sync engine created successfully")

        # Step 3: Define models directly here to avoid import issues
        print("\n3. Defining models directly...")

        # Import here to avoid the base.py issue
        from sqlmodel import Field, SQLModel
        import uuid
        from datetime import datetime
        from typing import Optional

        class UserBase(SQLModel):
            email: str = Field(unique=True, nullable=False, max_length=255)

        class User(UserBase, table=True):
            id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
            created_at: datetime = Field(default_factory=datetime.utcnow)
            updated_at: datetime = Field(default_factory=datetime.utcnow)

        class TaskBase(SQLModel):
            title: str = Field(nullable=False, max_length=255)
            description: Optional[str] = Field(default=None)
            completed: bool = Field(default=False)
            user_id: str = Field(foreign_key="user.id")

        class Task(TaskBase, table=True):
            id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
            created_at: datetime = Field(default_factory=datetime.utcnow)
            updated_at: datetime = Field(default_factory=datetime.utcnow)

        print("   [SUCCESS] Models defined successfully")

        # Step 4: Check SQLModel metadata
        print(f"\n4. SQLModel metadata contains {len(SQLModel.metadata.tables)} tables:")
        for table_name in SQLModel.metadata.tables.keys():
            print(f"   - {table_name}")

        # Step 5: Attempt to create tables
        print("\n5. Creating tables...")
        SQLModel.metadata.create_all(engine)
        print("   [SUCCESS] Tables created successfully")

        # Step 6: Inspect what tables were created
        print("\n6. Inspecting created tables...")
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"   Found tables: {tables}")

        # Step 7: Check for required tables
        required_tables = ['user', 'task']
        missing_tables = [table for table in required_tables if table not in tables]

        if missing_tables:
            print(f"   [ERROR] Missing tables: {missing_tables}")
            print("   This indicates that the table creation is not working properly.")
            return False
        else:
            print("   [SUCCESS] All required tables exist")

        # Step 8: Check columns in user table
        if 'user' in tables:
            user_columns = inspector.get_columns('user')
            user_column_names = [col['name'] for col in user_columns]
            print(f"   User table columns: {user_column_names}")

            required_user_cols = ['id', 'email', 'created_at', 'updated_at']
            missing_user_cols = [col for col in required_user_cols if col not in user_column_names]

            if missing_user_cols:
                print(f"   [ERROR] Missing columns in user table: {missing_user_cols}")
                return False
            else:
                print("   [SUCCESS] User table has all required columns")

        # Step 9: Check columns in task table
        if 'task' in tables:
            task_columns = inspector.get_columns('task')
            task_column_names = [col['name'] for col in task_columns]
            print(f"   Task table columns: {task_column_names}")

            required_task_cols = ['id', 'title', 'description', 'completed', 'user_id', 'created_at', 'updated_at']
            missing_task_cols = [col for col in required_task_cols if col not in task_column_names]

            if missing_task_cols:
                print(f"   [ERROR] Missing columns in task table: {missing_task_cols}")
                return False
            else:
                print("   [SUCCESS] Task table has all required columns")

        # Step 10: Test basic connection with a simple query
        print("\n7. Testing database connection with a simple query...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            val = result.scalar()
            print(f"   Query result: {val}")
            if val == 1:
                print("   [SUCCESS] Database connection working properly")
            else:
                print("   [ERROR] Database connection issue")
                return False

        print("\n[SUCCESS] ALL DIAGNOSTICS PASSED!")
        print("   Database is properly configured and tables are created.")
        return True

    except Exception as e:
        print(f"\n[ERROR] ERROR during diagnostic test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = direct_diagnostic_test()
    sys.exit(0 if success else 1)