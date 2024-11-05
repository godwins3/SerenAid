import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from engine.core import get_recommended_resources, get_related_concepts, get_emotion
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# Read environment variables
client = OpenAI()

@app.route('/api/v1/message', methods=['POST'])
def handle_message():
    user_message = request.json.get('message')

    if not user_message:
        logging.error("No message provided in the request.")
        return jsonify({'error': 'No message provided.'}), 400

    try:
        # Get emotion from the user message
        emotion = get_emotion(user_message)
        
        # Get related concepts from the user message
        related_concepts = get_related_concepts(user_message)

        # Prepare the prompt with related concepts
        related_concepts_text = ', '.join(related_concepts)
        prompt = (
            f"You are a virtual therapist. Engage in a supportive conversation with the user. "
            f"The user feels {emotion}. Related concepts are: {related_concepts_text}. "
            f"User says: {user_message}"
        )

        # Generate a response from OpenAI API
        output = client.chat.completions.create(
            model="gpt-4",  # Make sure to use a valid model name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}  # Use the dynamic prompt here
            ]
        )

        # Get the generated message from the response
        generated_message = output.choices[0].message.content
        print('Openai output: ', generated_message)
        
        # Get recommended resources
        resources = get_recommended_resources(emotion)

        return jsonify({
            'message': generated_message,
            'resources': resources,
            'related_concepts': related_concepts
        })
    
    except Exception as e:
        logging.error(f"Error while processing the message: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)
