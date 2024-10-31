from neo4j import GraphDatabase

class KnowledgeGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_related_concepts(self, message):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n:Concept)-[:RELATED_TO]->(related:Concept)
                WHERE n.name = $message
                RETURN related.name AS concept
            """, message=message)
            return [record["concept"] for record in result]

# Instantiate and use the KnowledgeGraph class
knowledge_graph = KnowledgeGraph("neo4j://localhost:7687", "neo4j", "your_password")

def get_related_concepts(message):
    return knowledge_graph.get_related_concepts(message)

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

