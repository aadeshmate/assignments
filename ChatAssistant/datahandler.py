import json
import chromadb
from sentence_transformers import SentenceTransformer

class DataHandler:
    def __init__(self,db_path="./chroma_db"):
        self.embedding_model=SentenceTransformer('all-MiniLM-L6-v2')
        self.chroma_client=chromadb.PersistentClient(path=db_path)
        self.collection=self.chroma_client.get_or_create_collection(name="fitness_faq")

    def process_store(self,data):
        ids,embeddings,documents,metadata=[],[],[],[]
        for i,item in enumerate(data):
            paragraphs = item["answer"].split('\n\n')
            # print(paragraphs)
            for j,para in enumerate(paragraphs):
                if not para.strip() :
                    continue
                
                chunk_text = f"Question: {item['question']}\nAnswer: {para.strip()}"
                embeddings.append(self.embedding_model.encode(chunk_text).tolist())
                ids.append(f"{i}_{j}")
                documents.append(chunk_text)
                metadata.append({"source":item["source"],"question":item["question"]})
        self.collection.add(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadata)
        # print(metadata)
        print(f"Stored {len(ids)}")

    def retrieve(self,query,top_k=2):
        print(query)
        query_emb=self.embedding_model.encode(query).tolist()
        results = self.collection.query(query_embeddings = [query_emb],n_results = top_k)
        return results["documents"][0],results["metadatas"][0]

if __name__ == "__main__":
    
    with open("faqs.json","r") as f:
        handler = DataHandler()
        handler.process_store(json.load(f))





