import React, { useState, useMemo } from 'react';
import { useFBCall } from '../hooks';

// Move configuration outside component to prevent recreation
const DEVICE_ID = Math.random().toString(36).substring(2, 15);
const CALL_CONFIG = {
  device_id: DEVICE_ID,
  prompt: "Hello, you are an AI companion. Respond to the users message using the following json schema: { 'my response': string }",
  responseHandlerUrl: "http://localhost:5000/handle-responses",
  twilioBackend: "https://managerdev.therapybuddy.org"
};

function CallControl() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Use the static config object
  const { isConnected, startCall, endCall } = useFBCall(CALL_CONFIG);

  const handleStartCall = async () => {
    try {
      setIsLoading(true);
      setError(null);
      await startCall();
    } catch (err) {
      setError(err.message || 'Failed to start call');
    } finally {
      setIsLoading(false);
    }
  };

  const handleEndCall = async () => {
    try {
      setIsLoading(true);
      setError(null);
      await endCall();
    } catch (err) {
      setError(err.message || 'Failed to end call');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="call-control">
      <h2>Call Control</h2>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <div className="button-group">
        <button 
          onClick={handleStartCall}
          disabled={isConnected || isLoading}
        >
          {isLoading ? 'Loading...' : 'Start Call'}
        </button>

        <button 
          onClick={handleEndCall}
          disabled={!isConnected || isLoading}
        >
          {isLoading ? 'Loading...' : 'End Call'}
        </button>
      </div>

      <div className="status">
        Status: {isConnected ? 'Connected' : 'Disconnected'}
      </div>
    </div>
  );
}

export default CallControl; 