from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from core.models import User
from core.database import db
from sqlalchemy import func

auth_bp = Blueprint('auth', __name__)

# --- LOGIN ROUTE ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').lower().strip()
        password = request.form.get('password')
        company = request.form.get('company').strip() # Case sensitive rakh sakte hain ya lower
        
        # 👇 QUERY CHANGE: Ab hum Email AUR Company dono se user dhoond rahe hain
        # func.lower use kar rahe hain taake 'Google' aur 'google' same maane jayen
        user = User.query.filter(
            func.lower(User.email) == email, 
            func.lower(User.company_name) == func.lower(company)
        ).first()
        
        if user and user.check_password(password):
            login_user(user)
            if user.role == 'super_admin':
                return redirect(url_for('admin_bp.super_admin_dashboard'))
            
            elif user.role == 'admin':
                return redirect(url_for('admin_bp.company_admin_dashboard')) # 👈 New Route
            
            else:
                return redirect(url_for('home'))
        else:
            flash('Login Failed. Check Company Name, Email or Password.', 'error')
            
    return render_template('login.html')

# --- REGISTER ROUTE ---
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email').lower().strip()
        password = request.form.get('password')
        company = request.form.get('company').strip()

        # 👇 CHECK: Kya Is Company mein Ye Email pehle se hai?
        existing_user = User.query.filter(
            func.lower(User.email) == email, 
            func.lower(User.company_name) == func.lower(company)
        ).first()

        if existing_user:
            flash(f'Email already registered in {company}.', 'error')
            return redirect(url_for('auth.register'))

        # Create New User
        new_user = User(email=email, role='user', company_name=company)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration Successful! Please Login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Error: {e}', 'error')

    return render_template('register.html')

# ... (Logout aur Super Admin wale routes same rahenge) ...
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/create-super-admin')
def create_super_admin():
    # Super Admin ka koi duplicate nahi ho sakta System company mein
    if User.query.filter_by(role="super_admin").first():
        return "Super Admin already exists!"
    
    user = User(email="super@admin.com", role="super_admin", company_name="System_Owner")
    user.set_password("super123")
    db.session.add(user)
    db.session.commit()
    return "✅ Super Admin Created!"