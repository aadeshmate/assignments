import os
from ollama import Client
from config import MODEL_NAME,DEFAULT_TEMPERATURE,HOSTNAME



def read_file_text(filename:str) ->str:
    WORKDIR = os.path.dirname(os.path.abspath(__file__))
    safe_path = os.path.join(WORKDIR,filename)
    if not os.path.exists(safe_path):
        return f"File {filename} not found"

    with open(safe_path,"r") as file:
        return file.read()


def summarize_text_file(filename:str) -> str:
    document = read_file_text(filename)
    client = Client(HOSTNAME)
    try:
        response = client.chat(
            model = MODEL_NAME,
            messages = [{
                "role" : "user",
                "content" : f"Summarize the file in 3 sentences {document}"
            }]
        )

    except Exception as e:
        print("Exception ", e)

   
    return response['message']['content']


def ask_from_file(filename:str,question:str) -> str : 
    document = read_file_text(filename)
    client = Client(HOSTNAME)
    try:
        response = client.chat(
            model = MODEL_NAME,
            messages = [{
                "role" : "user",
                "content" : f"Answer the question i.e {question} in this document : {document} . If answer is not present please say i don't know"
            }]

        )
    except Exception as e:
        print("Exception ", e)
    
    return response['message']['content']

def explain_file(filename:str) -> str :
    document = read_file_text(filename)
    print("filename" , filename)
    client = Client(HOSTNAME)
    try:
        response = client.chat(
            model = MODEL_NAME,
            messages = [{
                "role" : "user",
                "content" : f"Explain this file properly in 3-5 sentences Document : {document}"
            }]
        )

    except Exception as e:
        print("Exception ", e)
    
    return response['message']['content']
    



FILE_SUMMARIZER_TOOL_SCHEMA = {
    "type" : "function",
    "function" : {
        "name" : "summarize_text_file",
        "description" : "summarize text file in 2- 3 senetences",
        "parameters" : {
            "type" : "object",
            "properties" : {
                "filename" : {
                    "type" : "string",
                    "description" : "Path from where file read is done"
                }
            },
            "required" : ["filename"]
        }

    }
}

ASK_TOOL_SCHEMA_SCHEMA = {
    "type" : "function",
    "function" : {
        "name" : "ask_from_file",
        "description" : "Answer the question given by user in the document",
        "parameters" : {
            "type" : "object",
            "properties" : {
                "filename" : {
                    "type" : "string",
                    "description" : "Path from where file read is done",
                },
                "question" : {
                    "type" : "string",
                    "description" : "Answer this question from the file"
                }
            },
            "required" : ["filename","question"]
        }
        
    }
}


EXPLAIN_FILE_TOOL = {
    "type" : "function",
    "function" : {
        "name" : "explain_file",
        "description" : "Explain the document in 2-3 lines properly",
        "parameters" : {
            "type" : "object",
            "properties" : {
                "filename" : {
                    "type" : "string",
                    "description" : "Path from where file read is done"
                }
            },
            "required" : ["filename"]
        }
       
    }
}

TOOL_REGISTRY = {
    "summarize_text_file" : summarize_text_file,
    "ask_from_file": ask_from_file,
    "explain_file":explain_file
}