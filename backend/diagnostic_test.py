#!/usr/bin/env python3
"""
Diagnostic test script to verify database connectivity and table creation
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from sqlalchemy import create_engine, inspect, text
from sqlmodel import SQLModel
from src.config.settings import settings
from src.models.user import User
from src.models.task import Task

def diagnostic_test():
    print("=== DATABASE DIAGNOSTIC TEST ===")

    # Step 1: Check if DATABASE_URL is present
    print(f"1. DATABASE_URL present: {bool(settings.database_url)}")
    if not settings.database_url or settings.database_url == "postgresql://user:password@localhost/dbname":
        print("   ❌ DATABASE_URL is not properly configured. Please check your .env file.")
        return False

    # Replace postgresql:// with postgresql+asyncpg:// for async operations
    # But for sync operations (table creation), we'll use the original
    print(f"   Database URL: {'*' * len(settings.database_url)}")

    try:
        # Step 2: Create a sync engine for table creation
        print("\n2. Creating sync engine for table operations...")
        sync_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
        sync_url = sync_url.replace("postgresql+psycopg://", "postgresql://")

        # Use the original URL if it's already in the correct format
        engine = create_engine(sync_url, echo=True)
        print("   ✓ Sync engine created successfully")

        # Step 3: Check if models are imported properly
        print("\n3. Checking model imports...")
        print(f"   User model: {User}")
        print(f"   Task model: {Task}")
        print("   ✓ Models imported successfully")

        # Step 4: Check SQLModel metadata
        print(f"\n4. SQLModel metadata contains {len(SQLModel.metadata.tables)} tables:")
        for table_name in SQLModel.metadata.tables.keys():
            print(f"   - {table_name}")

        # Step 5: Attempt to create tables
        print("\n5. Creating tables...")
        SQLModel.metadata.create_all(engine)
        print("   ✓ Tables created successfully")

        # Step 6: Inspect what tables were created
        print("\n6. Inspecting created tables...")
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"   Found tables: {tables}")

        # Step 7: Check for required tables
        required_tables = ['user', 'task']
        missing_tables = [table for table in required_tables if table not in tables]

        if missing_tables:
            print(f"   ❌ Missing tables: {missing_tables}")
            return False
        else:
            print("   ✓ All required tables exist")

        # Step 8: Check columns in user table
        if 'user' in tables:
            user_columns = inspector.get_columns('user')
            user_column_names = [col['name'] for col in user_columns]
            print(f"   User table columns: {user_column_names}")

            required_user_cols = ['id', 'email', 'created_at', 'updated_at']
            missing_user_cols = [col for col in required_user_cols if col not in user_column_names]

            if missing_user_cols:
                print(f"   ❌ Missing columns in user table: {missing_user_cols}")
                return False
            else:
                print("   ✓ User table has all required columns")

        # Step 9: Check columns in task table
        if 'task' in tables:
            task_columns = inspector.get_columns('task')
            task_column_names = [col['name'] for col in task_columns]
            print(f"   Task table columns: {task_column_names}")

            required_task_cols = ['id', 'title', 'description', 'completed', 'user_id', 'created_at', 'updated_at']
            missing_task_cols = [col for col in required_task_cols if col not in task_column_names]

            if missing_task_cols:
                print(f"   ❌ Missing columns in task table: {missing_task_cols}")
                return False
            else:
                print("   ✓ Task table has all required columns")

        # Step 10: Test basic connection with a simple query
        print("\n7. Testing database connection with a simple query...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            val = result.scalar()
            print(f"   Query result: {val}")
            if val == 1:
                print("   ✓ Database connection working properly")
            else:
                print("   ❌ Database connection issue")
                return False

        print("\n✅ ALL DIAGNOSTICS PASSED!")
        print("   Database is properly configured and tables are created.")
        return True

    except Exception as e:
        print(f"\n❌ ERROR during diagnostic test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = diagnostic_test()
    sys.exit(0 if success else 1)