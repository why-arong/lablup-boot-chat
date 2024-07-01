import React, { useState, useEffect, useRef } from 'react';
import './Chat.css';

const Chat = ({ onLogout }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const messagesEndRef = useRef(null);
  const ws = useRef(null);

  useEffect(() => {
    const websocket = new WebSocket('ws://localhost:8080/ws');

    websocket.onopen = () => {
      console.log('WebSocket connection opened');
      setIsLoading(false);
    };

    websocket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        setMessages((prevMessages) => [...prevMessages, message]);
      } catch (error) {
        console.error('Error parsing message:', error);
      }
    };

    websocket.onclose = (event) => {
      console.log('WebSocket connection closed:', event);
      setIsLoading(true);
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsLoading(false);
    };

    ws.current = websocket;

    return () => {
      if (ws.current && ws.current.readyState === WebSocket.OPEN) {
        ws.current.close();
      }
    };
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = () => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN && newMessage.trim()) {
      const message = { content: newMessage };
      ws.current.send(JSON.stringify(message));
      setNewMessage('');
    } else {
      console.error('WebSocket is not open or message is empty');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    const options = { hour: '2-digit', minute: '2-digit', hour12: true };
    return date.toLocaleTimeString([], options);
  };

  return (
    <div className="chat-container">
      <h2>Chat Room</h2>
      <button onClick={onLogout} className="logout-button">Logout</button>
      {isLoading ? (
        <div className="loading">Connecting...</div>
      ) : (
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className="message">
              <span className="message-username">{msg.username}:</span>
              <span className="message-content">{msg.content}</span>
              <span className="message-timestamp">{formatTimestamp(msg.timestamp)}</span>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      )}
      <div className="message-input">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message"
          disabled={isLoading}
        />
        <button onClick={handleSendMessage} disabled={isLoading}>Send</button>
      </div>
    </div>
  );
};

export default Chat;
