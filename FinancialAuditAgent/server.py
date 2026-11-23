from mcp.server.fastmcp import FastMCP
import os
import json
import ast
import csv


mcp = FastMCP("This is Financial Audit project")

@mcp.tool()


def read_csv_expenses()->str:
    WORKDIR = os.path.dirname(os.path.abspath(__file__))
    safe_path = os.path.join(WORKDIR,"expenses.csv")
    print(safe_path)
    if not os.path.exists(safe_path):
        return "File not found"

    try:
        with open(safe_path,"r") as file:
            return file.read()

    except Exception as e:
        return f"File error {e}"

@mcp.tool()
def get_budget_limit(category:str)->str:
    WORKDIR = os.path.dirname(os.path.abspath(__file__))
    safe_path = os.path.join(WORKDIR,"Budget.json")

    print("---"*50,safe_path)
    if not os.path.exists(safe_path):
        return "File not found"


    try:
        with open(safe_path,"r") as file:
            budgets = json.load(file)

        if category not in budgets:
            return f"Category not present"
        
        return str(budgets[category])

    except Exception as e:
        return e


@mcp.tool()
def calculate_math(expression:str)->str:
    try:
        node = ast.parse(expression,mode='eval')
        return str(eval(compile(node,'<string','eval')))
    except Exception as e:
         return "Error as {e}"


# read_csv_expenses("expenses.csv")
# get_budget_limit("budget.json","Entertainment")
# calculate_math("200/200 + 300/300 + 1 + 1")


if __name__ == "__main__":
    mcp.run()
