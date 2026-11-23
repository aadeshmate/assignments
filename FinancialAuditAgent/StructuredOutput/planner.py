from tools.state import SubTask,AgentState
import ollama
from config import TEMPERATURE,MODEL_NAME
import json
from mcp.client.session import ClientSession
async def execute_subtask_with_mcp(current_task:SubTask,state:AgentState,session:ClientSession,ollama_tools:list):
    messages = [
        {
            "role": "system",
            "content": """
            You are a Financial Audit Agent.

            Available MCP tools:
            - read_csv_expenses: Reads expenses.csv only.
            - get_budget_limit: Reads category budgets from Budget.json.
            - calculate_math: Performs calculations.

            Rules:
            1. For expense data, use read_csv_expenses.
            2. For budget data, use get_budget_limit.
            3. Never try to read budgets from expenses.csv.
            4. Use previous completed task results.
            5. Do not invent data.
            6. Use MCP tools whenever required.
            
            """
        },
        {
            "role":"user",
            "content":f"""
                Overall Goal : {state.user_goal}
                Previosuly Completed Task and Findings  : {state.get_completed_context()}
                Current Task To Execute: {current_task.description}
            """
        }
    ]

    for _ in range(3):
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            tools=ollama_tools,
            options={
                "temperature":TEMPERATURE
            }
        )
       
        print(response["message"].model_dump_json(indent=4))
        if not response.message.tool_calls:
            current_task.result = response.message.content
            current_task.status = "completed"
            return current_task


        messages.append(response["message"])
        if response.get("message",{}).get("tool_calls"):
            for tool_call in response["message"]["tool_calls"]:
                func_name = tool_call["function"]["name"]
                func_args = tool_call["function"]["arguments"]

                tool_result = await session.call_tool(func_name,arguments=func_args)


                print("*"*40)

                print(tool_result)

                raw_output = tool_result.content[0].text

                

                messages.append({
                    
                    "role":"tool",
                    "tool_name": func_name,
                    "content":raw_output
                })

    current_task.result = "Execution stopped: maximum tool-call iterations reached."
    current_task.status = "failed"

    return current_task



