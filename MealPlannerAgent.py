from typing import Dict, Generator, Optional
import openai
import json

class MealPlannerAgent():
    def __init__(self, session_id: str, chat_histories: Dict[str, list]):
        # Configure OpenAI client
        self.client = openai.OpenAI(api_key='your-api-key')
        self.system_message = "You are a nutritionist that talks to the user to help them plan their meals."
        self.session_id = session_id
        self.chat_histories = chat_histories

    def generate_stream(self, detected_speech: str, system_message: Optional[str] = None) -> Generator[str, None, None]:
        """
        This function will guide the primary conversation.
        Generate streaming response from OpenAI API with optional system message.
        """
        try:

            print("detected_speech:", detected_speech)
            # Create streaming response from OpenAI
            messages = []
            if self.session_id in self.chat_histories:
                messages = self.chat_histories[self.session_id]
            
            prompt = self.system_message
            messages = [{"role": "system", "content": prompt}] + messages    
            
            messages_plus_current = messages + [{
                "role": "user",
                "content": detected_speech
            }]
            
            print("Sending messages to OpenAI:", messages_plus_current)
            
            stream = self.client.chat.completions.create(
                model="gpt-4o",
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

    def process_response(self, user_message: str, llm_response: str):
        '''
        Update the user grocery list based on the conversaiton
        '''
        print("Run more LLM calls here to update the users grocery list based on the conversation")

        

        grocery_list_updater_response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are a grocery list updater. You update the users grocery list based on the conversation. Output their updated grocery list in JSON format."}] + self.chat_histories[self.session_id],
            temperature=0.7,
            max_tokens=150,
            response_format={"type": "json_object"}
        )

        print("Updated grocery list:", grocery_list_updater_response.choices[0].message.content)