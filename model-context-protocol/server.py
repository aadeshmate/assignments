#fast mxp -> json rcp

import ast
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math and File server")

@mcp.tool()
def calc_math(expression:str) -> str:
    try:
        node = ast.parse(expression,mode='eval')
        return str(eval(compile(node,'<string>','eval')))
    except Exception as e:
        return f"Err {e}"

@mcp.tool()
def read_file(filepath:str) -> str:
    try:
        with open(filepath,'r') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file{e}"


if __name__=="__main__":
    mcp.run()


    




