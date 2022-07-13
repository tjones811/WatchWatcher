from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model


class Show:
    db = 'belt_schema'
    def __init__(self,data): 
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.user = {}


    @staticmethod
    def validate_show(form_data):
        is_valid = True

        if len(form_data['title']) < 3:
            flash('Please enter a longer title')
            is_valid = False

        if len(form_data['network']) < 3:
            flash('Please enter a longer network name')
            is_valid = False

        if len(form_data['description']) < 3:
            flash('Please enter a longer description')
            is_valid = False

        if len(form_data['release_date']) < 1:
            flash('Please enter a valid date')
            is_valid = False

        

        
        return is_valid


    @classmethod
    def add_new(cls, data):

        query = 'INSERT INTO shows(title,network,release_date,description,created_at,updated_at,user_id) VALUES(%(title)s,%(network)s,%(release_date)s,%(description)s,NOW(),NOW(),%(user_id)s)'

        results = connectToMySQL(cls.db).query_db(query,data)

        return results

    @classmethod
    def get_all(cls):

        

        query = 'SELECT * FROM shows;'

        results = connectToMySQL(cls.db).query_db(query)

        shows = []

        for show in results:
            shows.append(cls(show))
            
        return shows

    @classmethod
    def get_one(cls,data):

        query = 'SELECT * FROM shows LEFT JOIN users ON users.id = shows.user_id WHERE shows.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)

        show = cls (results[0])

        user_data = {
            'id' : results[0]['users.id'],
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'email' : results[0]['email'],
            'password' : results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at']
        }

        user_instance = user_model.User(user_data)
        show.user = user_instance

        return show


    @classmethod
    def update(cls,data):
        
        query = 'UPDATE shows SET title = %(title)s,network = %(network)s,release_date = %(release_date)s,description = %(description)s,updated_at = NOW() WHERE id = %(show_id)s '
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def delete(cls,data):

        query = 'DELETE FROM shows WHERE id = %(id)s'

        results = connectToMySQL(cls.db).query_db(query,data)

        return results



