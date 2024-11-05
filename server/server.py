import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from engine.core import get_recommended_resources, get_related_concepts, detect_emotion # get_emotion
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI()

# In-memory storage for conversation history
conversation_history = {}

@app.route('/api/v1/message', methods=['POST'])
def handle_message():
    user_id = request.json.get('userId')  # Assume each request includes a user_id
    user_message = request.json.get('message')

    if not user_message:
        logging.error("No message provided in the request.")
        return jsonify({'error': 'No message provided.'}), 400

    if not user_id:
        logging.error("No user_id provided in the request.")
        return jsonify({'error': 'No user_id provided.'}), 400

    try:
        # Get emotion from the user message
        emotion = detect_emotion(user_message)
        
        # Get related concepts from the user message
        related_concepts = get_related_concepts(user_message)
        related_concepts_text = ', '.join(related_concepts)

        # Prepare the conversation history for the prompt
        if user_id not in conversation_history:
            conversation_history[user_id] = []

        # Append the user's message to the conversation history
        conversation_history[user_id].append({"role": "user", "content": user_message})

        # Create a dynamic prompt including emotion and related concepts
        dynamic_prompt = (
            f"The user feels {emotion}. Related concepts are: {related_concepts_text}.\n"
            f"User says: {user_message}"
        )

        # Prepare messages for the OpenAI API call
        messages = [
            {"role": "system", "content": "You are a virtual therapist. Engage in a supportive conversation with the user."},
            {"role": "user", "content": dynamic_prompt}
        ] + conversation_history[user_id]

        # Generate a response from OpenAI API
        output = client.chat.completions.create(
            model="gpt-4",  # Make sure to use a valid model name
            messages=messages
        )

        # Get the generated message from the response
        generated_message = output.choices[0].message.content
        conversation_history[user_id].append({"role": "assistant", "content": generated_message})
        
        # Get recommended resources
        resources = get_recommended_resources(emotion)

        return jsonify({
            'message': generated_message,
            'emotion': emotion,
            'resources': resources,
            'related_concepts': related_concepts
        })
    
    except Exception as e:
        logging.error(f"Error while processing the message: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)
