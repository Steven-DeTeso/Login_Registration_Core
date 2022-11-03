import re
from flask_app import app, bcrypt
from flask_app.models.user import User
from flask import render_template, request, redirect, session, flash # etc

@app.route('/')
def r_home_page():
    return render_template('index.html')

@app.route('/register/user', methods=['POST'])
def f_register_user():
    if User.validate_user_register(request.form):
        data = {
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'email': request.form.get('email'),
        'password': bcrypt.generate_password_hash(request.form.get('password'))
        }
        User.save(data)
        return redirect('/login/success')
    return redirect('/')

@app.route('/login/user', methods=['POST'])
def f_login_user():
    data = {'email': request.form.get('email')}
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash('Invalid Email entereted', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form.get('password')):
        flash('Invalid Password entered', 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id # comes back as object so we use dot notation to access fields
    return redirect('/login/success')

@app.route('/login/success')
def r_success():
    if 'user_id' not in session:
        return redirect('/log_out')
    data = {
        'id': session['user_id']
    }
    return render_template('success.html', user = User.get_user_by_id(data))

@app.route('/log_out')
def rd_log_out():
    session.clear()
    return redirect('/')