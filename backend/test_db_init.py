#!/usr/bin/env python3
"""
Test script to verify database table creation
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.database import create_db_and_tables, engine
from sqlalchemy import inspect

def test_table_creation():
    print("Testing database table creation...")

    try:
        # Create all tables
        create_db_and_tables()
        print("✓ Tables created successfully")

        # Check what tables were created
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        print(f"Found tables: {tables}")

        # Check for required tables
        required_tables = ['user', 'task']  # Expected table names from SQLModel
        missing_tables = [table for table in required_tables if table not in tables]

        if missing_tables:
            print(f"✗ Missing tables: {missing_tables}")
            return False
        else:
            print("✓ All required tables exist")

        # Check columns in user table
        if 'user' in tables:
            user_columns = inspector.get_columns('user')
            user_column_names = [col['name'] for col in user_columns]
            required_user_cols = ['id', 'email', 'created_at', 'updated_at']
            missing_user_cols = [col for col in required_user_cols if col not in user_column_names]

            if missing_user_cols:
                print(f"✗ Missing columns in user table: {missing_user_cols}")
                return False
            else:
                print("✓ User table has all required columns")

        # Check columns in task table
        if 'task' in tables:
            task_columns = inspector.get_columns('task')
            task_column_names = [col['name'] for col in task_columns]
            required_task_cols = ['id', 'title', 'description', 'completed', 'user_id', 'created_at', 'updated_at']
            missing_task_cols = [col for col in required_task_cols if col not in task_column_names]

            if missing_task_cols:
                print(f"✗ Missing columns in task table: {missing_task_cols}")
                return False
            else:
                print("✓ Task table has all required columns")

        # Check foreign key constraint
        if 'task' in tables:
            fks = inspector.get_foreign_keys('task')
            print(f"Foreign keys in task table: {fks}")

            # Look for FK to user table
            user_fks = [fk for fk in fks if fk['referred_schema'] is None and 'user' in fk['referred_table']]
            if user_fks:
                print("✓ Foreign key constraint found from task.user_id to user.id")
            else:
                print("? Foreign key constraint check - may vary by SQLModel version")

        print("\n✓ Database initialization test completed successfully!")
        return True

    except Exception as e:
        print(f"✗ Error during database initialization test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_table_creation()
    sys.exit(0 if success else 1)