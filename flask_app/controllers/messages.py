from flask_app import app
from flask import render_template, redirect, request, session, flash 
from flask_app.models.message import Message

@app.route('/send_message/<int:id>', methods=['POST'])
def send_message(id):
    data = {
        'content':request.form['content'],
        'sender_id': session['user_id'],
        'receiver_id':id
    }
    Message.create_message(data)
    
    return redirect('/dashboard')