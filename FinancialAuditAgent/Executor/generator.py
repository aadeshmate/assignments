from tools.state import AgentState
from config import MODEL_NAME,TEMPERATURE
import ollama
def generate_final_answer(state:AgentState)->str:
    print("---------------------",state.get_next_pending_task())

    completed_tasks=state.get_completed_context()


    prompt = f"""
        Overall Goal: {state.user_goal}

        Completed Task Results:{completed_tasks}

        Write the final budget status summary in plain text.
        Use only facts and numbers already in the completed task results.
        Do not write code, imports, functions, or tool-call JSON.
        Do not invent numbers.
    """

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{
            "role":"user",
            "content":prompt
        }],
        options={
            "temperature":TEMPERATURE
        }

    )


    return response["message"]["content"]
   