import React, { useState } from 'react';
import axios from 'axios';
import EmailList from './components/EmailList';
import EmailFilter from './components/EmailFilter';

function App() {
  const [emails, setEmails] = useState([]);

  const syncEmails = async () => {
    try {
      const response = await axios.get('/sync-emails', {
        params: {
          username: 'user@example.com',  
          password: 'password123',
          imap_server: 'imap.gmail.com'
        }
      });
      setEmails(response.data);  
    } catch (error) {
      console.error('Error syncing emails:', error);
    }
  };

  return (
    <div className="App">
      <h1>Email Sync Dashboard</h1>
      <button onClick={syncEmails}>Sync Emails</button>
      <EmailFilter />
      <EmailList emails={emails} />
    </div>
  );
}

export default App;
