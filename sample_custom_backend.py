from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import json
from typing import Dict, Generator, Optional
from pydantic import BaseModel
from MealPlannerAgent import MealPlannerAgent
from threading import Thread

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

# Pydantic models for request validation
class ChatRequest(BaseModel):
    session_id: str
    detected_speech: str
    prompt_identifier: Optional[str] = None

class ProcessResponse(BaseModel):
    session_id: str
    user_message: str
    llm_response: str

@app.get("/")
def hello_world():
    return {"message": "Hello World"}

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
            # Replace this with the generate_stream function from the agent you want to use.
            MealPlannerAgent(request.session_id, chat_histories).generate_stream(request.detected_speech, system_message),
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

        # Start a new thread to process the response to not block the voice infrastructure
        # You can run other agents in the background like this as well.
        process_response_thread = Thread(target=MealPlannerAgent(session_id, chat_histories).process_response, args=(user_message, llm_response))
        process_response_thread.start()

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
