from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import openai
import json
from typing import Dict, Generator, Optional
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store chat histories in memory (in production, you'd want to use a database)
chat_histories: Dict[str, list] = {}

# Store prompt identifier to system message mapping
prompt_map: Dict[str, str] = {}

# Configure OpenAI client
client = openai.OpenAI(api_key='your-api-key')

# Pydantic models for request validation
class ChatRequest(BaseModel):
    session_id: str
    detected_speech: str
    prompt_identifier: Optional[str] = None

class ProcessResponse(BaseModel):
    session_id: str
    user_message: str
    llm_response: str

def generate_stream(session_id: str, detected_speech: str, system_message: Optional[str] = None) -> Generator[str, None, None]:
    """
    Generate streaming response from OpenAI API with optional system message.
    """
    try:
        # Create streaming response from OpenAI
        messages = []
        if session_id in chat_histories:
            messages = chat_histories[session_id]
        
        # Add system message if provided
        if system_message:
            messages = [{"role": "system", "content": system_message}] + messages
        
        messages_plus_current = messages + [{
            "role": "user",
            "content": detected_speech
        }]
        
        print("Sending messages to OpenAI:", messages_plus_current)
        
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=messages_plus_current,
            stream=True,
            temperature=0.7,
            max_tokens=150
        )

        # Stream the response chunks
        assistant_message = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                assistant_message += content
                print("Generated content chunk:", content)
                ## VERY IMPORTANT: ALWAYS YIELD IN THIS EXACT FORMAT. DO NOT CHANGE THIS LINE BELOW.
                yield f"data: {json.dumps({'content': content})}\n\n"

    except Exception as e:
        print(f"Error in generate(): {str(e)}")
        error_msg = json.dumps({'error': str(e)})
        yield f"data: {error_msg}\n\n"

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        if not request.session_id or not request.detected_speech:
            return JSONResponse(
                status_code=400,
                content={'error': 'Missing required fields'}
            )

        system_message = None
        if request.prompt_identifier:
            # First check the local prompt_map
            system_message = prompt_map.get(request.prompt_identifier)
            
            # If not in local map, return error
            if system_message is None:
                return JSONResponse(
                    status_code=404,
                    content={'error': f'No system message found for prompt identifier: {request.prompt_identifier}'}
                )

        return StreamingResponse(
            generate_stream(request.session_id, request.detected_speech, system_message),
            media_type='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
                'Access-Control-Allow-Origin': '*',
            }
        )

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={'error': str(e)}
        )

@app.post("/process_response")
async def process_response(request: ProcessResponse):
    try:
        session_id = request.session_id
        user_message = request.user_message
        llm_response = request.llm_response

        # Get or create chat history
        if session_id not in chat_histories:
            chat_histories[session_id] = []

        # Add both messages to chat history
        chat_histories[session_id].append({
            "role": "user",
            "content": user_message
        })
        chat_histories[session_id].append({
            "role": "assistant",
            "content": llm_response
        })

        print(chat_histories[session_id])

        # You can run any further processing here, 
        # but remember to do any long lasting processing a thread or in the background 
        # to not block the voice infrastructure from continuing to talk to the user.

        return JSONResponse(
            content={'status': 'success', 'message': 'Chat history updated'},
            status_code=200
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={'error': str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    print("Starting server on http://localhost:5000")
    uvicorn.run(app, host="0.0.0.0", port=5000)
