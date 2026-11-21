import ollama
from agentstate import TaskPlan,SubTask
from typing import List

def decompose_plan(user_goal:str,available_tool:List[str],model:str='llama3.2')->List[SubTask]:
    prompt = f"""You are AI Task decomposer Break down the following goal {user_goal}
    Available tools : {available_tool},
    Rules : 
    - Each Subtask must be atomic and exectuable
    - Order them by logic
    - Set Status to Pending for which result is null
    """

    messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ]

    response = ollama.chat(
        model=model,
        messages=messages,
        format=TaskPlan.model_json_schema(),
        options={
            "temperature":0.7
        }
    )

    plan = TaskPlan.model_validate_json(response["message"]["content"])
    return plan.tasks