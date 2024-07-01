import React, { useState } from 'react';
import './Signup.css';

const Signup = ({ onToggleSignup }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [signupMessage, setSignupMessage] = useState('');

  const handleSignup = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        setSignupMessage('');
        onToggleSignup();
      } else {
        const errorData = await response.json();
        setSignupMessage(errorData.message || 'Failed to sign up.');
      }
    } catch (error) {
      setSignupMessage('An error occurred. Please try again.');
    }
  };

  return (
    <div id="signupPage">
      <h2>Sign Up</h2>
      <form id="signupForm" onSubmit={handleSignup}>
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
        <button type="submit">Sign Up</button>
        <p id="signupMessage" className="error-message">{signupMessage}</p>
        <p>Already have an account? <a href="#" onClick={onToggleSignup}>Login</a></p>
      </form>
    </div>
  );
};

export default Signup;
