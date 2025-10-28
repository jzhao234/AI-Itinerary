from sqlalchemy import text
from app.core.database import engine

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("✅ Connected to:", result.scalar())
except Exception as e:
    print("❌ Connection failed:", e)
