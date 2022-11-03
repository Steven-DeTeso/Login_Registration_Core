from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
# classes and interacting with the database 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user_register(form_data:dict[str, str]) -> bool:
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('login_registration_schema').query_db(query, form_data)
        if len(result) >= 1:
            flash("Email is already registered in system!", 'register')
            is_valid = False
        if len(form_data.get('first_name')) < 3:
            flash("First name has to be longer or not left blank!", 'register')
            is_valid = False
        if len(form_data.get('last_name')) < 3:
            flash("Last name has to be longer or not left blank!", 'register')
            is_valid = False
        if len(form_data.get('email')) <= 0:
            flash("Valid email is required!", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(form_data.get('email')):
            flash("Email is in the wrong format!", 'register')
            is_valid = False
        if len(form_data.get('password')) < 8:
            flash("Your password isn't long enough! It has to be at least 8 characters!", 'register')
            is_valid = False
        if form_data.get('password') != form_data.get('confirm_password'):
            flash('Passwords must match!', 'register')
            is_valid = False
        if form_data.get('radio') != 'verified':
            flash('Please verify you are not a robot!', 'register')
            is_valid = False
        return is_valid


    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());
        """
        return connectToMySQL('login_registration_schema').query_db(query, data)
    
    @classmethod
    def get_user_by_email(cls, data:dict):
        query = """SELECT * 
        FROM users 
        WHERE email = %(email)s;"""
        result = connectToMySQL('login_registration_schema').query_db(query, data)
        if len(result) < 1: 
            return False
        return cls(result[0])

    @classmethod 
    def get_user_by_id(cls, data):
        query = """ SELECT * 
        FROM users 
        WHERE id = %(id)s
        """
        result = connectToMySQL('login_registration_schema').query_db(query, data)
        return cls(result[0])
