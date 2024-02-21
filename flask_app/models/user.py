from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class User:
    db_name = "rethinkgreen_db"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.profile_pic = data['profile_pic']
        self.points = data['points']
    
    
    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(data['email']) < 3:
            flash("Email must be at least 3 characters.")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        return is_valid
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (name, email, password) VALUES (%(name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def update_profile_pic(cls, data):
        query = "UPDATE users SET profile_pic = %(image)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update_points(cls, data):
        query = "UPDATE users SET points = %(points)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
        
    @classmethod
    def update_wheel_points(cls, data):
        query = "UPDATE users SET points = %(points)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)