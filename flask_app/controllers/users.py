from flask_app import app
from flask_app.models.user import User
from flask import render_template, request, redirect # etc

@app.route('/')
def r_home_page():
    return render_template('index.html')

@app.route('/register/user', methods=['POST'])
def f_register_user():
    if not User.validate_user_register(request.form):
        return redirect('/')
    # User.save(request.form)
    # return redirect('/')