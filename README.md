# SerenAid

SerenAid is a virtual therapy assistant that leverages advanced AI models and knowledge graphs to provide supportive and insightful interactions with users. The application is built using Flask for the backend and Bootstrap for the frontend, integrated with OpenAI for generating conversational responses and IBM Tone Analyzer for emotional tone detection. Neo4j is used for managing a knowledge graph to enhance response accuracy and relevance.

## Features

- **Conversational AI**: Utilizes OpenAI's language model for generating therapeutic responses.
- **Emotional Tone Analysis**: Analyzes the user's emotional tone using IBM Tone Analyzer.
- **Knowledge Graph Integration**: Uses Neo4j to store and query a knowledge graph for contextually rich responses.
- **Bootstrap Frontend**: Clean and responsive UI built with Bootstrap.

## Prerequisites

- Docker
- Docker Compose
- Neo4j

## Setup and Installation

### Clone the Repository

```sh
git clone https://github.com/godwins3/serenaid.git
cd serenaid
```

### Environment Variables

Create a .env file in the root directory and add the following environment variables:

```sh
OPENAI_API_KEY=your_openai_api_key
IBM_TONE_ANALYZER_API_KEY=your_ibm_tone_analyzer_api_key
IBM_TONE_ANALYZER_URL=your_ibm_tone_analyzer_url
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password
```

### Docker Setup

1. Build the docker container

```sh
docker-compose build
```

2. Run the docker container

```sh
docker-compose up
```

### Access the Application

Open your browser and navigate to <http://localhost:5000>.

## Project Structure

```sh
serenaid/
│
├── .env                    # Environment variables
├── .gitignore              # Git ignore file
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker configuration for Flask app
├── requirements.txt        # Python dependencies
├── server/                 # Flask server code
│   ├── __init__.py
│   ├── server.py              # Main Flask app
|   ├── wsgi.py
│   ├── engine/  # Knowledge graph utilities and Resource recommendation logic
│   │   └── core.py
│   └── templates/
│       ├── base.html       # Base HTML template
│       └── index.html      # Main HTML template
└── static/                 # Static files (CSS, JS)
    ├── css/
    │   └── styles.css
    └── js/
        └── script.js
```

## API endpoints

POST /api/message
Handles user messages, performs tone analysis, generates a response using OpenAI, and fetches related concepts from the knowledge graph.

Request:

```sh
{
  "message": "I feel stressed about my exams."
}
```

Response:

```sh
{
  "message": "It sounds like you're feeling overwhelmed. It's important to take breaks and organize your study schedule. How can I assist you further?",
  "resources": [
    "Resource 1",
    "Resource 2"
  ],
  "related_concepts": [
    "Stress management",
    "Study tips"
  ]
}
```

## Technologies Used

- Backend: Flask, Neo4j
- Frontend: Bootstrap
- AI Models: OpenAI, IBM Tone Analyzer
- Containerization: Docker, Docker Compose

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

```javascript

Replace placeholders such as `your_openai_api_key`, `your_ibm_tone_analyzer_api_key`, `your_ibm_tone_analyzer_url`, and `your_neo4j_password` with your actual credentials and secrets. Also, update the GitHub repository URL in the "Clone the Repository" section to your repository's URL.
```
