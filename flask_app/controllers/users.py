from flask_app import app, bcrypt
from flask_app.models.user import User
from flask import render_template, request, redirect # etc

@app.route('/')
def r_home_page():
    return render_template('index.html')

@app.route('/register/user', methods=['POST'])
def f_register_user():
    print(request.form)
    if User.validate_user_register(request.form):
        data = {
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'email': request.form.get('email'),
        'password': bcrypt.generate_password_hash(request.form.get('password'))
        }
        User.save(data)
        return redirect('/register/success')
    return redirect('/')

@app.route('/register/success')
def r_success():
    return render_template('success.html')

@app.route('/go_back')
def rd_go_back():
    return redirect('/')