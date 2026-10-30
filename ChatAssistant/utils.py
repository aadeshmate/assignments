import ollama

def build_prompt(user_question,retrieved_chunks):
    prompt = "Answer the user's question using only the provided context.\n\n context: \n\n"
    for chunk in retrieved_chunks:
        prompt+=f"{chunk}\n--\n"
    prompt+=f"\nUser Question : {user_question}\n"

    return prompt

def get_ollama_response(prompt,model='qwen3:4b'):
    response = ollama.chat(
        model=model,
        messages=[
            {
                "role" : "user",
                "content" : prompt
            }
        ]
    )

    text = response['message']['content']+"\n\n"

    return text
