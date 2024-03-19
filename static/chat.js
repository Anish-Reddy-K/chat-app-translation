document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const username = '{{ username }}';
    const rooms = JSON.parse('{{ rooms | tojson | safe }}');

    function joinRoom(room) {
        socket.emit('join', { 'username': username, 'room': room });
    }

    joinRoom('default');

    const roomSelect = document.getElementById('room-select');
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    roomSelect.addEventListener('change', () => {
        const selectedRoom = roomSelect.value;
        chatMessages.innerHTML = '';
        joinRoom(selectedRoom);
    });

    sendButton.addEventListener('click', () => {
        const message = messageInput.value.trim();
        if (message !== '') {
            socket.emit('message', { 'username': username, 'message': message, 'room': roomSelect.value });
            messageInput.value = '';
        }
    });

    socket.on('message', data => {
        const messageElement = document.createElement('div');
        messageElement.innerHTML = `<strong>${data.username}:</strong> ${data.message}`;
        
        // Check if the message belongs to the current room
        const currentRoom = roomSelect.value;
        if (currentRoom === data.room) {
            chatMessages.appendChild(messageElement);
        }
    });
});
