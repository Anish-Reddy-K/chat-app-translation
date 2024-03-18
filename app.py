from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = {'user': 'password', 'user2': 'password2'}  # Simple in-memory authentication

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if users.get(username) == password:
        return redirect(url_for('chat', username=username))
    else:
        return 'Invalid username or password'

@app.route('/chat/<username>')
def chat(username):
    return render_template('chat.html', username=username)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('message', {'username': 'System', 'message': username + ' has entered the room.'}, room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('message', {'username': 'System', 'message': username + ' has left the room.'}, room=room)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    room = data['room']
    emit('message', {'username': username, 'message': message}, room=room)

if __name__ == "__main__":
    socketio.run(app)
