from sqlalchemy import text

from src.db.session import engine

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("✅ Database connected successfully!")
except Exception as e:
    print("❌ Database connection failed!")
    print(e)