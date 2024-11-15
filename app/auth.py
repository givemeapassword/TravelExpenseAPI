from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User
import logging

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            logging.getLogger().info(f'User {username} logged in successfully.')
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main_bp.index'))  # Перенаправляем на главную страницу
        else:
            logging.getLogger().warning(f'Failed login attempt for user {username}.')
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            logging.getLogger().warning(f'Attempt to register existing user {username}.')
            flash('User already exists', 'error')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        
        logging.getLogger().info(f'New user {username} registered successfully.')
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logging.getLogger().info(f'User {current_user.username} logged out.')
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
