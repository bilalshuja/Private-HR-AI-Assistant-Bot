from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from core.models import User
from core.database import db
from core.decorators import super_admin_required,admin_required
from sqlalchemy import func

# Blueprint banaya
admin_bp = Blueprint('admin_bp', __name__)

# 👇 Dashboard Route (Sirf Super Admin dekh sakta hai)
@admin_bp.route('/super-admin', methods=['GET', 'POST'])
@super_admin_required
def super_admin_dashboard():
    
    # --- 1. Admin Create Karne Ki Logic ---
    if request.method == 'POST':
        email = request.form.get('email').lower().strip()
        password = request.form.get('password')
        company = request.form.get('company').strip()
        
        # Check duplicate (Same company same email nahi hona chahiye)
        existing = User.query.filter(
            func.lower(User.email) == email, 
            func.lower(User.company_name) == func.lower(company)
        ).first()

        if existing:
            flash(f'User already exists in {company}!', 'error')
        else:
            # ✅ Naya Admin Banao
            new_admin = User(email=email, role='admin', company_name=company)
            new_admin.set_password(password)
            db.session.add(new_admin)
            db.session.commit()
            flash(f'✅ Admin created for {company}!', 'success')
            return redirect(url_for('admin_bp.super_admin_dashboard'))

    # --- 2. List Show Karna ---
    # Saare Admins ki list uthao taake Super Admin dekh sake kis kis ko banaya hai
    all_admins = User.query.filter_by(role='admin').all()
    
    return render_template('super_admin.html', admins=all_admins)

@admin_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
@admin_required # 🔒 Sirf Admin aa sakta hai
def company_admin_dashboard():
    return render_template('company_admin.html', user=current_user)