import React, { useState } from 'react';
import Login from './Login';
import Signup from './Signup';
import Chat from './Chat';
import './App.css';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showSignupPage, setShowSignupPage] = useState(false);

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
