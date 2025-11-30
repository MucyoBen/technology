const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.static('public')); // Aha niho tuzashyira frontend

let participants = {};

io.on('connection', socket => {
    console.log('New user connected:', socket.id);

    socket.on('join', name => {
        participants[socket.id] = name;
        io.emit('participants', participants);
    });

    socket.on('message', msg => {
        io.emit('message', { from: participants[socket.id], text: msg });
    });

    socket.on('signal', data => {
        // data: { to, signal }
        io.to(data.to).emit('signal', { from: socket.id, signal: data.signal });
    });

    socket.on('disconnect', () => {
        delete participants[socket.id];
        io.emit('participants', participants);
        console.log('User disconnected:', socket.id);
    });
});

server.listen(3000, () => console.log('Server running on port 3000'));
