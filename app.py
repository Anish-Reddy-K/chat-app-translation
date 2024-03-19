from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
from google.cloud import translate_v2 as translate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = {'anish': 'passforanish', 'cyril': 'passforcyril'}  # Simple in-memory authentication
rooms = ['default', 'room1', 'room2']  # List of available rooms
room_messages = {}  # Dictionary to store messages for each room
translate_client = translate.Client()  # Initialize the Google Cloud Translate client

# Function to translate messages
def translate_message(message, target_language):
    translation = translate_client.translate(message, target_language=target_language)
    return translation['translatedText']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if users.get(username) == password:
        return redirect(url_for('chat', username=username, room='default'))
    else:
        return 'Invalid username or password'

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('message', {'username': 'System', 'message': username + ' has entered the room.', 'room': room}, room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('message', {'username': 'System', 'message': username + ' has left the room.', 'room': room}, room=room)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    room = data['room']
    target_language = data.get('target_language')

    if target_language and target_language != 'original':
        message = translate_message(message, target_language)

    emit('message', {'username': username, 'message': message, 'room': room}, room=room)
    
    # Store the message in the room's message list
    if room not in room_messages:
        room_messages[room] = []
    room_messages[room].append({'username': username, 'message': message})

@app.route('/chat/<username>/<room>')
def chat(username, room):
    if room not in room_messages:
        room_messages[room] = []
    return render_template('chat.html', username=username, room=room, rooms=rooms, messages=room_messages[room])

if __name__ == "__main__":
    socketio.run(app)
