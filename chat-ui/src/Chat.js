import React, { useEffect, useState, useRef } from 'react';

const ChatRoom = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const ws = useRef(null);

  useEffect(() => {
    const websocket = new WebSocket('ws://localhost:8080/ws');

    websocket.onopen = () => {
      console.log('WebSocket connection opened');
    };

    websocket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages((prevMessages) => {
        // Check if the message is already in the state
        const messageExists = prevMessages.some(
          (msg) => msg.username === message.username && msg.content === message.content && msg.timestamp === message.timestamp
        );
        if (!messageExists) {
          return [...prevMessages, message];
        }
        return prevMessages;
      });
    };

    websocket.onclose = (event) => {
      console.log('WebSocket connection closed:', event);
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.current = websocket;

    return () => {
      if (ws.current && ws.current.readyState === WebSocket.OPEN) {
        ws.current.close();
      }
    };
  }, []);

  const handleSendMessage = () => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN && newMessage.trim()) {
      const message = { content: newMessage };
      ws.current.send(JSON.stringify(message));
      setNewMessage('');
    } else {
      console.error('WebSocket is not open or message is empty');
    }
  };

  return (
    <div>
      <h2>Chat Room</h2>
      <div id="messages">
        {messages.map((msg, index) => (
          <div key={index}>
            <strong>{msg.username}:</strong> {msg.content}
            <span> {new Date(msg.timestamp).toLocaleTimeString()}</span>
          </div>
        ))}
      </div>
      <input
        type="text"
        value={newMessage}
        onChange={(e) => setNewMessage(e.target.value)}
        placeholder="Type your message"
      />
      <button onClick={handleSendMessage}>Send</button>
    </div>
  );
};

export default ChatRoom;
