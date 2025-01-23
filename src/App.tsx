import React from 'react';
import './App.css';
import { useNavigate } from 'react-router-dom';
import { Button } from '@mui/material';
import Box from '@mui/material/Box';
import EnhancedTable from './components/EnhancedTable';
import Header from './components/Header';
import { useEffect } from 'react';

function App() {
  const navigate = useNavigate();

  useEffect(() => {
    // Check if Service Workers and Push API are supported
    if ('serviceWorker' in navigator && 'PushManager' in window) {
      navigator.serviceWorker.register('/sw.js').then((swReg) => {
      //navigator.serviceWorker.register('/sw.js', { scope: 'http://localhost:5001' }).then((swReg) => { //geht nicht der scope muss gleich dem frontend sein.
        console.log('Service Worker registered', swReg);

        // Request notification permission
        Notification.requestPermission().then((permission) => {
          if (permission === 'granted') {
            subscribeUser(swReg);
          } else {
            console.error('User denied push notifications.');
          }
        });
      }).catch((error) => {
        console.error('Service Worker registration failed:', error);
      });
    } else {
      console.error('Push messaging is not supported in your browser.');
    }
  }, []);

  const subscribeUser = async (swReg: ServiceWorkerRegistration) => {
    try {
      const subscription = await swReg.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: 'BCcugnAXkyYu6Ci9G0FbmeYD3EzvUoNTCxqpFo1TCHSB9-iErdH2v3FYYWHNngZKXVRVFP-D00m5li1g_DAmCe4' // Replace with your VAPID public key
      });

      console.log('User subscribed:', subscription);

      // Send subscription to the server
      //Eintrag ins package.json: ,"proxy": "http://127.0.0.1:5001"
      await fetch('http://localhost:5001/subscribe', {
      //await fetch('http://172.18.0.7:5001/subscribe', {  
      //await fetch('/subscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(subscription)
      });
    } catch (error) {
      console.error('Failed to subscribe the user:', error);
    }
  };


  return (
    <div className="App">
      <Header/>
      <EnhancedTable/>
      <Box sx={{ mt: 2 }}>
        <Button variant="contained" onClick={() => {navigate('/add');}}>Hinzufügen</Button>
      </Box>
    </div>
  );
}

export default App;