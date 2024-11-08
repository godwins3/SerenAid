import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from engine.core import get_recommended_resources, get_related_concepts, detect_emotion, add_concept, add_relationship
from pymongo import MongoClient
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI()

# Initialize MongoDB client
mongo_uri = os.getenv('MONGO_URI')
mongo_client = MongoClient(mongo_uri)
db = mongo_client['chatbot']
conversation_collection = db['conversations']

therapists_file_path = 'server\engine\therapists\persona.json'
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

therapists = read_json(therapists_file_path)

@app.route('/api/v1/message', methods=['POST'])
def handle_message():
    user_id = request.json.get('userId')
    user_message = request.json.get('message')
    selected_therapist = request.json.get('therapist', 'emily')  # Default to Emily if not specified

    if not user_message:
        logging.error("No message provided in the request.")
        return jsonify({'error': 'No message provided.'}), 400

    if not user_id:
        logging.error("No user_id provided in the request.")
        return jsonify({'error': 'No user_id provided.'}), 400

    try:
        # Detect emotion from the user message
        emotion = detect_emotion(user_message)
        
        # Get related concepts from the user message
        related_concepts = get_related_concepts(selected_therapist, user_id, user_message)
        related_concepts_text = ', '.join(related_concepts)

        # Add new concepts and relationships to the knowledge graph
        add_concept(selected_therapist, user_id, user_message)
        for concept in related_concepts:
            add_relationship(selected_therapist, user_id, user_message, concept)

        # Retrieve conversation history from MongoDB
        conversation = conversation_collection.find_one({"user_id": user_id})
        if not conversation:
            conversation = {"user_id": user_id, "history": []}
        
        # Append the user's message to the conversation history
        conversation['history'].append({"role": "user", "content": user_message})

        # Create a dynamic prompt including emotion, related concepts, and therapist persona
        therapist_persona = therapists[selected_therapist]["persona"]
        dynamic_prompt = (
            f"{therapist_persona}\n"
            f"The user feels {emotion}. Related concepts are: {related_concepts_text}.\n"
            f"User says: {user_message}"
        )

        # Prepare messages for the OpenAI API call, limiting to the last few messages to save tokens
        history = conversation['history'][-10:]  # Limit history to the last 10 messages
        messages = [
            {"role": "system", "content": "You are a virtual therapist. Engage in a supportive conversation with the user."},
            {"role": "user", "content": dynamic_prompt}
        ] + history

        # Generate a response from OpenAI API
        output = client.chat.completions.create(
            model="gpt-4",  # Use a cheaper model if possible
            messages=messages,
            max_tokens=150  # Limit the response length to save costs
        )

        # Get the generated message from the response
        generated_message = output.choices[0].message.content
        conversation['history'].append({"role": "assistant", "content": generated_message})

        # Update the conversation history in MongoDB
        conversation_collection.update_one({"user_id": user_id}, {"$set": conversation}, upsert=True)

        # Get recommended resources
        resources = get_recommended_resources([emotion])

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
