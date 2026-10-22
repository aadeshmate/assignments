import os
from ollama import Client 
from config import HOSTNAME,MODEL_NAME
from tool import FILE_SUMMARIZER_TOOL_SCHEMA,ASK_TOOL_SCHEMA_SCHEMA,EXPLAIN_FILE_TOOL,TOOL_REGISTRY


WORKDIR = os.path.dirname(os.path.abspath(__file__))
filename = "notes.txt"

while True:
    user_prompt = input("ENTER 1 : SUMMARIZE \n ENTER 2 : ASK FOR QUESTION \n ENTER 3 : EXPLAIN ")
    client = Client(HOSTNAME)

    safe_path = os.path.join(WORKDIR,filename)

    if user_prompt=="1":
        message = {
            "role" : "user",
            "content" : f"summarize the file {safe_path}"
        }
    elif user_prompt=="2":
        question = input("Ask any Question ? ")
        message = {
            "role" : "user",
            "content" : f"Answerr the {question} from the given file filepath : {safe_path}" 
        }
    elif user_prompt=="3":
        message = {
            "role" : "user",
            "content" : f"Explain the file  filepath : {safe_path}"
        }
    else:
        break

    response = client.chat(
        model = MODEL_NAME,
        messages = [message],
        tools = [FILE_SUMMARIZER_TOOL_SCHEMA,
        ASK_TOOL_SCHEMA_SCHEMA,
        EXPLAIN_FILE_TOOL]
    )

    if response.get("message",{}).get("tool_calls"):
        for tool_call in response["message"]["tool_calls"]:
            tool_name = tool_call['function']['name']
            tool_args = tool_call['function']['arguments']


            tool_function = TOOL_REGISTRY.get(tool_name)
            tool_result = tool_function(**tool_args)

            print(f"Tool Name : {tool_name} result : {tool_result}")













