from mcp.client.session import ClientSession
from agentstate import AgentState,SubTask
import ollama
import json
async def execute_subtask_with_mcp(
        session:ClientSession,
        ollama_tools:list,
        state:AgentState,
        current_task:SubTask,
        model="llama3.2"
):
    system_prompt = "You are state aware MCP planner" \
    " use Provided tools and focus on current task" \
    "Call the tool for the task"

    user_prompt = f"""
        Overall Goal : {state.user_goal},
        Previosuly Completed Task and Findings  : {state.get_next_pending_task}
        Current Task To Execute: {current_task}
    """


    messages = [
         {   
            "role":"system",
            "content":system_prompt
         },
         {
             "role":"user",
             "content":user_prompt
         }
    ]

    for _ in range(3):
        response = ollama.chat(
            model=model,
            messages=messages,
            tools=ollama_tools
        )

        print(response["message"].model_dump_json(indent=4))
        
        if response.get("message",{}).get("tool_calls"):
            for tool_call in response["message"]["tool_calls"]:
                function_name = tool_call["function"]["name"]
                function_args = tool_call["function"]["arguments"]
        
                tool_result = await session.call_tool(function_name,arguments=function_args)
        
                        
        
                raw_output = tool_result.content[0].text
        
        
                messages.append(response['message'])
        
                messages.append({
                    "role":"tool",
                    "content":raw_output
                })
        

    current_task.result = "Execution stopped: maximum tool-call iterations reached."
    current_task.status = "completed"
            


