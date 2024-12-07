import React from 'react';
import './App.css';
import CallControl from './components/CallControl';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Voice Call App</h1>
        <CallControl />
      </header>
    </div>
  );
}

export default App;
