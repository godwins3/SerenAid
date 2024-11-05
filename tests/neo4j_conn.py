from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get Neo4j credentials from environment variables
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

def test_neo4j_conn():
    # Create a Neo4j driver instance
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    # Verify the connection
    try:
        with driver.session() as session:
            result = session.run("RETURN 1")
            for record in result:
                print(record)
        print("Connection successful")
    except Exception as e:
        print(f"Authentication failed: {e}")
    finally:
        driver.close()

if __name__=="__main__":
    test_neo4j_conn()