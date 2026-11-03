import json
import os
import ast

def read_local_file(filepath:str)->str:
    try:
        with open(filepath,'r') as file:
            return file.read()

    except Exception as e:
        print(e)

        return e

# '''  str={'name':'ABC','age':'28,'skills':['py','js']}
     # ast.literal_eval()->dictionary


     # 2+2

def calculate_math(expression:str)->str:
    try:
        node = ast.parse(expression,mode='eval')
        return str(eval(compile(node,'<string>','eval')))
    except Exception as e:
        return f"Error calculating:{str(e)}"


FILE_READER_TOOL = {
    "type" : "function",
    "function" : {
        "name" : "read_local_file",
        "description" : "",
        "parameters" : {
            "type" : "object",
            "description":"read the given file",
            "filepath" : {
                    "type" : "string",
                    "description" : "path of a file"

            },
            "required":["filepath"]
        }
    }
}

CALCULATOR_SCHEMA = {
    "type" : "function",
    "function" : {
        "name" : "calculate_math",
        "description" : "Evaluate the mathematical expression",
        "parameters" : {
            "type" : "object",
            "description" : "",
            "expression":{
                "type":"string",
                "description":"expression"
            }
        },
        "required":["expression"]
    }
}

TOOL_REGISTRY = {
    "read_local_file":read_local_file,
    "calculate_math":calculate_math
}

AVAILABLE_TOOL = [FILE_READER_TOOL,CALCULATOR_SCHEMA]


    