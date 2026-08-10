# scripts/reset_superadmin_password.py
from src.db.session import SessionLocal
from src.core.security import hash_password
from src.models.administration.user import User

NEW_PASSWORD = "superadmin123"

db = SessionLocal()
try:
    user = db.query(User).filter(User.username == "superadmin").first()
    if not user:
        raise SystemExit("superadmin not found")
    user.password_hash = hash_password(NEW_PASSWORD)
    db.commit()
    print(f"Password updated for user id={user.id}")
finally:
    db.close()