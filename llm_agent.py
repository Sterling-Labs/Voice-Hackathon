from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
import openai
import json
from typing import Dict, Generator

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store chat histories in memory (in production, you'd want to use a database)
chat_histories: Dict[str, list] = {}

# Configure OpenAI client
client = openai.OpenAI(api_key='')

def generate_stream(session_id: str, detected_speech: str) -> Generator[str, None, None]:
    """
    Replace this to create your own Agent
    """
    try:
        # Create streaming response from OpenAI
        messages = []
        if session_id in chat_histories:
            messages = chat_histories[session_id]
        
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
                yield f"data: {json.dumps({'content': content})}\n\n"
        
        yield f"data: [DONE]\n\n"

    except Exception as e:
        print(f"Error in generate(): {str(e)}")
        error_msg = json.dumps({'error': str(e)})
        yield f"data: {error_msg}\n\n"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        detected_speech = data.get('detected_speech')

        if not session_id or not detected_speech:
            return {'error': 'Missing required fields'}, 400

        response = Response(
            stream_with_context(generate_stream(session_id, detected_speech)),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
                'Access-Control-Allow-Origin': '*',
            }
        )
        return response

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return {'error': str(e)}, 500

@app.route('/process_response', methods=['POST'])
def process_response():
    data = request.get_json()
    session_id = data.get('session_id')
    user_message = data.get('user_message')
    llm_response = data.get('llm_response')

    if not all([session_id, user_message, llm_response]):
        return {'error': 'Missing required fields'}, 400

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

    # Return JSON response with proper content type
    return Response(
        json.dumps({'status': 'success', 'message': 'Chat history updated'}),
        status=200,
        mimetype='application/json'
    )


if __name__ == '__main__':
    print("Starting server on http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
