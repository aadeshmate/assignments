from mcp.server.fastmcp import FastMCP
import ast
import shutil
import os

mcp = FastMCP("This is Task Planner Project...")

@mcp.tool()
def get_disk_free_mb(path:str=".")->str:
    total, used, free = shutil.disk_usage(path)
    free_mb = round(free / (1024 * 1024), 2)

    return f"Free disk space: {free_mb} MB"

@mcp.tool()
def read_file_log(filename:str)->str:
    WORKDIR = os.path.dirname(os.path.abspath(__file__))
    safe_path = os.path.join(WORKDIR,filename)
    if not os.path.exists(safe_path):
        return f"File {filename} not found"
   
    with open(safe_path,"r") as file:
        return file.read()

@mcp.tool()
def calculate(expression:str)->str:
    try:
        node = ast.parse(expression,mode='eval')
        return str(eval(compile(node,'<string>','eval')))
    except Exception as e:
        return f"error : {e}"


if __name__ == "__main__":
    mcp.run()
