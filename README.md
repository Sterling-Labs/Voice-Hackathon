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

## Manage LLM Agent
## Single Prompt

### Prompt Registration API

The prompt registration endpoint allows you to store or update prompts in the database using an upsert operation. During the hackathon, this endpoint can be used to register prompts that will be used for your voice interactions.

### Endpoint
`POST /api/hackathon-register-prompt`

### Request Body
```
{
    "prompt_key": "string",    // Identifier for this specific prompt
    "prompt": "string",        // The actual prompt content
    "org_id": "string"        // Your team's unique identifier
}
```


### Important Note for Hackathon Teams

For the `org_id`, please use your team name followed by some random numbers to ensure uniqueness. For example:
coolteam12345
voicehackers98765
promptengineers44444
This doesn't need to be fancy - it just needs to be unique from other teams!

### Example Usage
```
await fetch('https://api.focusbuddy.ai/api/hackathon-register-prompt', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        prompt_key: "greeting",
        prompt: "Hello! I'm excited to help you today. What would you like to work on?",
        org_id: "coolteam12345"
    })
});
```
### Behavior
Behavior
- If a prompt with the same prompt_key and org_id already exists, it will be updated
- If no matching prompt exists, a new one will be created
- Each team can have multiple prompts with different prompt_key values
