from typing import List
from tools.state import SubTask,TaskPlan
import ollama
from config import MODEL_NAME,TEMPERATURE
def decompose_plan(user_goal:str,available_tools:List)->List[SubTask]:
    prompt = f"""
        You are a task decomposer for an Financial Audit Agent Project.
        Break the user's goal into small, ordered and executable subtasks.
        Each task should be specific and actionable.
        Generate tasks that can be executed using available MCP tools.
        Return tasks in the correct execution order.
        You are giving user goal : {user_goal}
        Available Tools : {available_tools}
    """


    messages = [{
        "role":"user",
        "content":prompt
    }]

    response = ollama.chat(
        model=MODEL_NAME,
        messages=messages,
        format=TaskPlan.model_json_schema()
    )


    plan = TaskPlan.model_validate_json(response["message"]["content"])

    return plan.tasks