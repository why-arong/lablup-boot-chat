import React, { useState, useEffect } from 'react';
import Login from './Login';
import Signup from './Signup';
import Chat from './Chat';
import './App.css';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showSignupPage, setShowSignupPage] = useState(false);

  useEffect(() => {
    const checkSession = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/session`, {
          method: 'GET',
          credentials: 'include',
        });

        if (response.ok) {
          setIsLoggedIn(true);
        }
      } catch (error) {
        console.error('Error checking session:', error);
      }
    };

    checkSession();
  }, []);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
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
        <Chat onLogout={handleLogout} />
      )}
    </div>
  );
};

export default App;
