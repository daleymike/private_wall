from sqlite3 import connect
from unittest import result
from flask import request
from flask_app.config.mysqlconnection import connectToMySQL

class Message:
    db = 'private_wall_schema'
    def __init__(self,data):
        self.id = data['id']
        self.content = data['content']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_message(cls,data):
        query = "INSERT INTO messages (content, sender_id, receiver_id) VALUES (%(content)s, %(sender_id)s, %(receiver_id)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
    @classmethod
    def get_messages(cls,data):
        query = "SELECT * FROM messages LEFT JOIN users ON sender_id = users.id WHERE receiver_id = %(receiver_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        return results

    # @classmethod
    # def get_sender(cls, data):
    #     query = "SELECT * FROM messages LEFT JOIN users on messages.sender_id = users.id"
    #     results = connectToMySQL(cls.db).query_db(query, data)
    #     print(results)
    #     return results

