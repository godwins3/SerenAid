import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from engine.core import get_recommended_resources, get_related_concepts, get_emotion

app = Flask(__name__)
CORS(app)

# Read environment variables
OpenAI.api_key = os.getenv('OPENAI_API_KEY')
neo4j_uri = os.getenv('NEO4J_URI')
neo4j_user = os.getenv('NEO4J_USER')
neo4j_password = os.getenv('NEO4J_PASSWORD')


@app.route('/api/v1/message', methods=['POST'])
def handle_message():
    user_message = request.json.get('message')

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

    # Get response from OpenAI
    response = OpenAI.Completion.create(
        engine='davinci',
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
    )
    assistant_message = response.choices[0].text.strip()

    # Get recommended resources
    resources = get_recommended_resources(emotion)

    return jsonify({
        'message': assistant_message,
        'resources': resources,
        'related_concepts': related_concepts
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
