from neo4j import GraphDatabase
import os
import logging
from transformers import pipeline
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

neo4j_uri = os.getenv('NEO4J_URI')
neo4j_user = os.getenv('NEO4J_USER')
neo4j_password = os.getenv('NEO4J_PASSWORD')

classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

class KnowledgeGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1")
                for record in result:
                    print(record)
            print("Connection successful")
        except Exception as e:
            print(f"Authentication failed: {e}")
            self.driver.close()

    def close(self):
        self.driver.close()

    def get_related_concepts(self, user_id, message):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u:User {id: $user_id})-[:INTERESTED_IN]->(n:Concept)-[:RELATED_TO]->(related:Concept)
                WHERE n.name = $message
                RETURN related.name AS concept
            """, user_id=user_id, message=message)
            return [record["concept"] for record in result]

    def add_concept(self, user_id, concept):
        with self.driver.session() as session:
            session.run("""
                MERGE (u:User {id: $user_id})
                MERGE (c:Concept {name: $concept})
                MERGE (u)-[:INTERESTED_IN]->(c)
            """, user_id=user_id, concept=concept)

    def add_relationship(self, user_id, concept1, concept2):
        with self.driver.session() as session:
            session.run("""
                MATCH (u:User {id: $user_id})-[:INTERESTED_IN]->(c1:Concept {name: $concept1})
                MERGE (c2:Concept {name: $concept2})
                MERGE (c1)-[:RELATED_TO]->(c2)
            """, user_id=user_id, concept1=concept1, concept2=concept2)

# Instantiate and use the KnowledgeGraph class
knowledge_graph = KnowledgeGraph(neo4j_uri, neo4j_user, neo4j_password)

def get_related_concepts(user_id, message):
    return knowledge_graph.get_related_concepts(user_id, message)

def add_concept(user_id, concept_name):
    knowledge_graph.add_concept(user_id, concept_name)

def add_relationship(user_id, concept1, concept2):
    knowledge_graph.add_relationship(user_id, concept1, concept2)

resources_database = {
    "Joy": ["https://www.positivepsychology.com/what-is-joy/", "https://www.psychologytoday.com/us/basics/joy"],
    "Anger": ["https://www.verywellmind.com/how-to-deal-with-anger-5098315", "https://www.helpguide.org/articles/relationships-communication/anger-management.htm"],
    "Fear": ["https://www.verywellmind.com/what-is-fear-2673944", "https://www.psychologytoday.com/us/basics/fear"],
    "Sadness": ["https://www.verywellmind.com/understanding-sadness-5112691", "https://www.psychologytoday.com/us/basics/sadness"],
    "Analytical": ["https://www.verywellmind.com/what-is-analytical-thinking-2795481", "https://www.psychologytoday.com/us/basics/analytical-thinking"],
    "Confident": ["https://www.verywellmind.com/what-is-self-confidence-2795868", "https://www.psychologytoday.com/us/basics/self-confidence"],
    "Tentative": ["https://www.verywellmind.com/tentative-language-communication-5195545", "https://www.psychologytoday.com/us/basics/tentative-language"],
}

def get_recommended_resources(tones):
    resources = []
    for tone in tones:
        if tone in resources_database:
            resources.extend(resources_database[tone])
    return resources

def detect_emotion(message):
    results = classifier(message)
    highest_score = 0
    highest_label = ""

    for result in results[0]:
        if result['score'] > highest_score:
            highest_score = result['score']
            highest_label = result['label']

    return highest_label



# from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
# from tensorflow.keras.models import load_model # type: ignore
# from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore

# def get_emotion(message):
#     base_path = os.path.dirname(os.path.abspath(__file__))
#     model_path = os.path.join(base_path, 'emo.keras')
#     loaded_model = load_model(model_path)

#     tokenizer = Tokenizer(num_words=50000)
#     sequences = tokenizer.texts_to_sequences([message])

#     # Pad the sequences to ensure consistent input size
#     padded_sequences = pad_sequences(sequences, maxlen=79)

#     # Make a prediction
#     prediction = loaded_model.predict(padded_sequences)
#     class_labels = ['Sadness', 'Joy', 'Love', 'Anger', 'Fear', 'Surprise']

#     # Get the index of the highest probability
#     predicted_index = prediction.argmax()

#     # Get the corresponding class label
#     predicted_label = class_labels[predicted_index]
#     print(predicted_label)
#     return predicted_label
