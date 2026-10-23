from pathlib import Path
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_BASE = os.path.join(BASE_DIR, "KnowledgeBase")


def load_documents():

    documents = {}

    folder = Path(KNOWLEDGE_BASE)
    

    for file in folder.glob("*.txt"):
        documents[file.name] = file.read_text(
            encoding="utf-8"
        )

    return documents

def retrieve(query):

    documents = load_documents()

    query = query.lower()

    for filename,description in documents.items():
        if query in description.lower():
            return filename,description


    return None,None