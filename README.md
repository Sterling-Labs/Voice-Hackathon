# Voice-Hackathon

## Index
- Start a call
  - React component
  - Phone Call
  - Desktop Microphone
- Manage LLM Agent
  - Single Prompt
  - Bring your own backend

## Starting a Call

### React Installation

```bash
npm install use-fb-call
```

### React Sample Usage
```bash
import { useFBCall, type FBConnection } from 'use-fb-call';
import { type FC } from 'react';

const MyComponent: FC = () => {
  const { isConnected, startCall, endCall, activeConnection } = useFBCall({
    device_id: "your_device_id",
    prompt: "Initial conversation prompt",
    responseHandlerUrl: "http://your-api.com/handle-responses"
  });

  const handleMute = () => {
    if (activeConnection) {
      activeConnection.mute(true);
    }
  };

  return (
    <div>
      <button onClick={startCall} disabled={isConnected}>
        Start Call
      </button>
      <button onClick={endCall} disabled={!isConnected}>
        End Call
      </button>
      <button onClick={handleMute} disabled={!activeConnection}>
        Mute
      </button>
    </div>
  );
};

export default MyComponent;
```
