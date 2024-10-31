import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from engine.core import get_recommended_resources, get_related_concepts

app = Flask(__name__)
CORS(app)

# Read environment variables
OpenAI.api_key = os.getenv('OPENAI_API_KEY')
ibm_tone_analyzer_api_key = os.getenv('IBM_TONE_ANALYZER_API_KEY')
ibm_tone_analyzer_url = os.getenv('IBM_TONE_ANALYZER_URL')
neo4j_uri = os.getenv('NEO4J_URI')
neo4j_user = os.getenv('NEO4J_USER')
neo4j_password = os.getenv('NEO4J_PASSWORD')


# IBM Tone Analyzer Configuration
tone_analyzer = ToneAnalyzerV3(
    version='2020-05-01',
    authenticator=IAMAuthenticator(ibm_tone_analyzer_api_key)
)
tone_analyzer.set_service_url(ibm_tone_analyzer_url)

@app.route('/api/message', methods=['POST'])
def handle_message():
    user_message = request.json.get('message')

    # Analyze the tone of the message
    tone_analysis = tone_analyzer.tone({'text': user_message}, content_type='application/json').get_result()
    tones = [tone['tone_name'] for tone in tone_analysis['document_tone']['tones']]

    # Get response from OpenAI
    response = OpenAI.Completion.create(
        engine='davinci',
        prompt=f"You are a virtual therapist. Engage in a supportive conversation with the user. The user feels {', '.join(tones)}. User says: {user_message}",
        max_tokens=150,
        temperature=0.7,
    )
    assistant_message = response.choices[0].text.strip()

    # Get resources and related concepts
    resources = get_recommended_resources(tones)
    related_concepts = get_related_concepts(user_message)

    return jsonify({
        'message': assistant_message,
        'resources': resources,
        'related_concepts': related_concepts
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
