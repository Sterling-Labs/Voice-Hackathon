import React, { useState, useMemo } from 'react';
import { useFBCall } from 'use-fb-call';

const SESSION_ID = Math.random().toString(36).substring(2, 15);

function CallControl() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Call with a single prompt
  const { isConnected, startCall, endCall, activeConnection} = useFBCall({
    session_id: SESSION_ID,
    org_id: "test",
    prompt_key: "test",
  });

  // Call with a custom backend
  // const { isConnected, startCall, endCall, activeConnection} = useFBCall({
  //   session_id: SESSION_ID,
  //   custom_llm_endpoint: "http://this-is-a-test-endpoint.com",
  // });

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