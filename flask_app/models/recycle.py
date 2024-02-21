from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Recycle:
    db_name = "rethinkgreen_db"
    def __init__(self, data):
        self.id = data['id']
        self.address = data['address']
        self.material = data['material']
        self.items = data['items']
        self.image = data['image']
        self.user_id = data['user_id']
        
        
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recycles (address, material, items, image, user_id) VALUES (%(address)s, %(material)s, %(items)s, %(image)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
        
    @staticmethod
    def validate_recycle(data):
        is_valid = True
        if data['totalItems'] is None or (int)(data['totalItems']) < 0:
            is_valid = False

        return is_valid