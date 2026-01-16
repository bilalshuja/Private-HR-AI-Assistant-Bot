import time
from app import app, db
from sqlalchemy import text

def init_database():
    with app.app_context():
        # Thoda wait karein taake DB container ready ho jaye
        print("⏳ Waiting for Database to start...")
        time.sleep(3) 
        
        try:
            # Connection check
            db.session.execute(text('SELECT 1'))
            print("✅ Database is Online.")
            
            # Tables create karein
            db.create_all()
            print("✅ Tables Created (if not existed).")
            
        except Exception as e:
            print(f"❌ Database Error: {e}")

if __name__ == "__main__":
    init_database()