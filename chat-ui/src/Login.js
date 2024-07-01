import React, { useState } from 'react';
import './Login.css';

const Login = ({ onLogin, onToggleSignup }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loginMessage, setLoginMessage] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
        credentials: 'include',
      });

      if (response.ok) {
        setLoginMessage('');
        onLogin();
      } else {
        const errorData = await response.json();
        setLoginMessage(errorData.message || 'Invalid username or password.');
      }
    } catch (error) {
      setLoginMessage('An error occurred. Please try again.');
    }
  };

  return (
    <div id="loginPage">
      <h2>Login</h2>
      <form id="loginForm" onSubmit={handleLogin}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit">Login</button>
        <p id="loginMessage" className="error-message">{loginMessage}</p>
        <p>Don't have an account? <a href="#" onClick={onToggleSignup}>Sign Up</a></p>
      </form>
    </div>
  );
};

export default Login;
