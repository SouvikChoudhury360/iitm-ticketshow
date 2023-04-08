from flask import Blueprint, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.dashboard'))

@auth.route("/signup")
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
        print("User already Exists")
        return redirect(url_for('auth.signup'))
    new_user = User(email=email, name=name, isAdmin=False , password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route("/adminAuth")
def adminAuth():
    return render_template('admin.html')

@auth.route('/adminAuth', methods=['POST'])
def adminAuth_post():
    password = request.form.get('password')
    user = User.query.filter_by(email="admin@ticketshow.co").first()
    if not user or not check_password_hash(user.password, password):
        new_user = User(email="admin@ticketshow.co", name="Admin", isAdmin=True , password=generate_password_hash("12345#", method='sha256'))
        db.session.add(new_user)
        db.session.commit()      
        user = new_user 
    
    if not user or not check_password_hash(user.password, password):
        return redirect('auth.adminAuth')
    
    login_user(user, remember=True)
    return redirect(url_for('main.adminDashboard'))


@ auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))