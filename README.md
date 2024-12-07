# Voice-Hackathon

We @ [FocusBuddy](https://focusbuddy.ai/) built one of the few consumer voice agents that users interact with for 4+ hours a day.
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
```bash
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

### Sample CURL Request
```bash
curl -X POST "https://hackathon.focusbuddy.ai/api/hackathon-register-prompt" \
-H "Content-Type: application/json" \
-d '{
  "org_id": "coolteam12345",
  "prompt_key": "builder-at-hackathon",
  "prompt": "You are a builder at a hackathon excited to build a voice AI project"
}'
```
Parameters:
- org_id: your team name followed by some random numbers to ensure uniqueness
- prompt_key: a unique identifier for this prompt
- prompt: the prompt content

### Behavior
- If a prompt with the same prompt_key and org_id already exists, it will be updated
- If no matching prompt exists, a new one will be created
- Each team can have multiple prompts with different prompt_key values

## Use your prompt in the `useFBCall` hook

You can now start a call using your prompt by specifying the org_id and prompt_key in the `useFBCall` hook.

### Sample Usage
```typescript
const {isConnected, startCall, endCall, activeConnection} = useFBCall({
    session_id: SESSION_ID,
    org_id: "coolTeam12345",
    prompt_key: "builder-at-hackathon",
});
```

# Agentic Voice Call with Custom Backend

While a single prompt is a great way to get started, with a custom backend, your recieve what the user has said each turn, and return to us whatever you want the voice agent to say in response. 
This way you can take what the user says, use LLMs to update your UI, run multiple prompts on it, change the prompt based on what the users input was, etc and then respond.

Here's how you can setup a custom backend.

## Quick Start with sample_custom_backend.py

1. `python3 -m venv env`
2. `source env/bin/activate`
3. `pip install -r requirements.txt`
4. Then run the sample custom backend: `python3 sample_custom_backend.py`


In this you'll see there are two endpoints;
- `/chat`: This is where you will recieve what the user said and you stream back your agents response.
- `/process_response`: This function is called after the AI has responded to the user. You can do any further processing you want here, but remember to do any long lasting processing a thread or in the background to not block the voice infrastructure from continuing to talk to the user.

In the sample_custom_backend you see a sample implementation of a meal planner agent that gives the user guidance on planner their meals in the `/chat` endpoint, and then updates the users grocery list based on the conversation in the `/process_response` endpoint.

You can make copies of the `MealPlannerAgent.py` and modify it to build your own agent.
If you're making a copy of `MealPlannerAgent.py`, you will need to get an OpenAI API key and put it in the `__init__`

## Use ngrok to create a public endpoint to your custom backend
You will need to use ngrok to create a public endpoint to your custom backend.
Just [make an account on their site and follow the setup instructions](https://dashboard.ngrok.com/get-started/setup/macos)

## Use your custom backend in the `useFBCall` hook
```typescript
const {isConnected, startCall, endCall, activeConnection} = useFBCall({
    session_id: SESSION_ID,
    custom_llm_endpoint: "http://your-custom-backend-endpoint.com",
});
```

# FAQs
## Muting and unmuting
You can mute and unmute the user by calling `activeConnection.mute(true)` and `activeConnection.mute(false)`
activeConnection is returned from the `useFBCall` hook and is null when there is no an active call.
It's a wrapper around the Twilio SDK's `Connection` object. You can see all the methods and properties available on it [here](https://www.twilio.com/docs/voice/sdks/javascript/v1/connection#method-reference).


