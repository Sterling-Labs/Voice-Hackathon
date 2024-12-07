# Voice-Hackathon

We @ FocusBuddy built one of the few consumer voice agents that users interact with for 4+ hours a day.
We wanted to make it easier for developers to build voice agents that work on the web and enable dynamic UIs on top of the voice call.

To do that, we're making this voice agent SDK available to you during the hackathon.

You will be able to spin up a website with a voice agent that your users can interact with.

# Index
- Start your first call
- Single Prompt Voice Call
- Agentic Voice Call with Custom Backend
- FAQs
  - Muting and unmuting

# Start your first call
You can try out a web voice call using our example in the `react-frontend` folder.

### Run our sample frontend:
```
cd react-frontend
npm install
npm start # This will run the app on http://localhost:3000
```

### Have a call
Click start call, and say "Hello" to the agent.

### Using your own frontend
When you are ready to use your own frontend, you can install `npm install use-fb-call` and follow the sample usage below and in `components/CallControl.js` in the `react-frontend` example.

All calls must have a `session_id` specified. This is any random string that becomes the identifier for the call. There must only be one call with a given session_id at a time.

# Single Prompt Voice Call

There's two basic steps to using your own prompt
1. Register your prompt with an org_id and prompt_key
2. Specify your org_id and prompt_key in the `useFBCall` hook

## Register your prompt

You are going to make a POST request to our endpoint specifying your prompt (prompt_value) and your org_id and a prompt_key - which is what you will use to refer to this prompt in the `useFBCall` hook.

### Endpoint
`POST https://hackathon.focusbuddy.ai/api/hackathon-register-prompt`

### Request Body
```
{
    "prompt_key": "string",    // Identifier for this specific prompt
    "prompt": "string",        // The actual prompt content
    "org_id": "string"        // Your team's unique identifier
}
```

### Sample CURL Request
```
curl -X POST "https://hackathon.focusbuddy.ai/api/hackathon-register-prompt" -H "Content-Type: application/json" -d '{"prompt_key": "builder-at-hackathon", "prompt": "You are a builder at a hackthon excited to build a voice AI project", "org_id": "coolteam12345"}'
```

### Org Id for hackathon teams
For the `org_id`, please use your team name followed by some random numbers to ensure uniqueness. For example:
coolteam12345
voicehackers98765
promptengineers44444
This doesn't need to be fancy - it just needs to be unique from other teams!

### Behavior
- If a prompt with the same prompt_key and org_id already exists, it will be updated
- If no matching prompt exists, a new one will be created
- Each team can have multiple prompts with different prompt_key values

## Use your prompt in the `useFBCall` hook

You can now start a call using your prompt by specifying the org_id and prompt_key in the `useFBCall` hook.

### Sample Usage
```
const {sConnected, startCall, endCall, activeConnection} = useFBCall({
    session_id: SESSION_ID,
    org_id: "coolTeam12345",
    prompt_key: "builder-at-hackathon",
});
```

# Agentic Voice Call with Custom Backend

While a single prompt is a great way to get started, with a custom backend, your recieve what the user has said each turn, and return to us whatever you want the voice agent to say in response. 

This way you can take what the user says, use LLMs to update your UI, run multiple prompts on it, change the prompt based on what the users input was, etc and then respond.

Here's how you can setup a custom backend.

## Quick Start with test.py
TODO: To be filled out

## Use ngrok to create a public endpoint to your custom backend
TODO: To be filled out

## Use your custom backend in the `useFBCall` hook
```
const {isConnected, startCall, endCall, activeConnection} = useFBCall({
    session_id: SESSION_ID,
    custom_llm_endpoint: "http://your-custom-backend-endpoint.com/endpoint",
});
```

# FAQs
## Muting and unmuting
You can mute and unmute the user by calling `activeConnection.mute(true)` and `activeConnection.mute(false)`
activeConnection is returned from the `useFBCall` hook and is null when there is no an active call.
It's a wrapper around the Twilio SDK's `Connection` object. You can see all the methods and properties available on it [here](https://www.twilio.com/docs/voice/sdks/javascript/v1/connection#method-reference).


