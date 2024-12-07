import aiohttp
import asyncio
import json

async def process_response(session, user_message, llm_response, session_id):
    url = 'http://localhost:5001/process_response'
    headers = {'Content-Type': 'application/json'}
    data = {
        'session_id': session_id,
        'user_message': user_message,
        'llm_response': llm_response
    }

    async with session.post(url, headers=headers, json=data) as response:
        result = await response.json()
        print("\nProcess response result:", result)

async def test_chat_endpoint():
    url = 'http://localhost:5001/chat'
    headers = {'Content-Type': 'application/json'}
    user_message = 'How can I help you?'
    session_id = 'test'
    
    data = {
        'session_id': session_id,
        'detected_speech': user_message
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            print("Receiving stream:")
            full_response = ""
            
            # Process the SSE stream
            async for line in response.content:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    try:
                        # Parse the JSON data from the event
                        event_data = json.loads(line[6:])  # Skip 'data: ' prefix
                        content = event_data['content']
                        print(content, end='', flush=True)
                        full_response += content
                    except json.JSONDecodeError:
                        print("Error decoding JSON from event:", line)
            
            print("\n\nFull response:", full_response)
            
            # After receiving the full response, process it
            await process_response(session, user_message, full_response, session_id)

if __name__ == "__main__":
    # Create and run the async event loop
    asyncio.run(test_chat_endpoint()) 