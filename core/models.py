from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from core.database import db
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    
    # 👇 CHANGE 1: 'unique=True' hata diya hai. Ab duplicate emails allow hain.
    email = db.Column(db.String(120), nullable=False)
    
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')
    company_name = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 👇 CHANGE 2: Ye Naya Rule hai (Email + Company mil kar unique honge)
    __table_args__ = (
        db.UniqueConstraint('email', 'company_name', name='_email_company_uc'),
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_super_admin(self):
        return self.role == 'super_admin'