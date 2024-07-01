import React, { useState, useEffect } from 'react';
import Login from './Login';
import Signup from './Signup';
import Chat from './Chat';
import './App.css';
import {API_URI} from './config';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showSignupPage, setShowSignupPage] = useState(false);
  const [username, setUsername] = useState('');

  useEffect(() => {
    const checkSession = async () => {
      try {
        const response = await fetch(`${API_URI}/session`, {
          method: 'GET',
          credentials: 'include',
        });

        if (response.ok) {
          const data = await response.json();
          setUsername(data.username);
          setIsLoggedIn(true);
        }
      } catch (error) {
        console.error('Error checking session:', error);
      }
    };

    checkSession();
  }, []);

  const handleLogin = (username) => {
    setIsLoggedIn(true);
    setUsername(username);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUsername('');
  };

  const toggleSignupPage = () => {
    setShowSignupPage(!showSignupPage);
  };

  return (
    <div className="container">
      {!isLoggedIn && !showSignupPage && (
        <Login onLogin={handleLogin} onToggleSignup={toggleSignupPage} />
      )}
      {!isLoggedIn && showSignupPage && (
        <Signup onToggleSignup={toggleSignupPage} />
      )}
      {isLoggedIn && (
        <Chat onLogout={handleLogout} username={username} />
      )}
    </div>
  );
};

export default App;
