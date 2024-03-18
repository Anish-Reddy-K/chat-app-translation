document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    // Get username from template
    // const username = '{{ username }}'; // Remove this line

    // Function to join a chat room
    function joinRoom(room) {
        socket.emit('join', { 'username': username, 'room': room });
    }

    // Function to leave a chat room
    function leaveRoom(room) {
        socket.emit('leave', { 'username': username, 'room': room });
    }

    // Join the default room when the page loads
    joinRoom('default');

    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    sendButton.addEventListener('click', () => {
        const message = messageInput.value.trim();
        if (message !== '') {
            socket.emit('message', { 'username': username, 'message': message, 'room': 'default' });
            messageInput.value = '';
        }
    });

    socket.on('message', data => {
        const messageElement = document.createElement('div');
        messageElement.innerHTML = `<strong>${data.username}:</strong> ${data.message}`;
        chatMessages.appendChild(messageElement);
    });
});
