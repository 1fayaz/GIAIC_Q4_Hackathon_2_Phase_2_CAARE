#!/usr/bin/env python3
"""
Test script to verify that the startup event runs properly
"""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Import the startup function and dependencies
from src.database import create_db_and_tables
from src.main import lifespan  # This should trigger the startup event

def test_startup_directly():
    """Test the startup function directly"""
    print("Testing startup function directly...")

    try:
        create_db_and_tables()
        print("✓ Startup function executed successfully")
        return True
    except Exception as e:
        print(f"✗ Startup function failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_startup_directly()
    if success:
        print("\n✓ Database initialization is working correctly!")
    else:
        print("\n✗ Database initialization has issues!")
        exit(1)