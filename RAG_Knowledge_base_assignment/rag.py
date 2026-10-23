from ollama import Client
import os
from getembedding import get_embedding
from cosinesimilarity import cosine_similarity
from retriever import load_documents
from config import HOSTNAME,MODEL_NAME




KnowledgeBase = load_documents() #dicitionary {"filename" : " ", "filename2"}

KB_EMBEDDING = {} 

for filename,description in KnowledgeBase.items():
    KB_EMBEDDING[filename] = get_embedding(description)



while True:
    user_input = input("\n You : ")

    if(user_input.lower() == "quit"):
        print("\n AI : Quitting ... Bye")

    QUERY_EMBEDDING = get_embedding(user_input)


    best_score = -1
    for filename,description in KB_EMBEDDING.items():
        score = cosine_similarity(description,QUERY_EMBEDDING)


        if score>best_score:
            best_score = score
            best_file = filename

    
    
        best_context = KnowledgeBase[best_file]

    



    # Create AI client
    client = Client( host = HOSTNAME)
    prompt = f"Answer the question using the following context.If the answer is not available in the context, say you don't know. : {best_context} question : {user_input}"


    response = client.chat(
        model = MODEL_NAME,
        messages = [{"role":"user","content":prompt}]
    )

    print(response['message']['content'])




     



