from agentstate import AgentState
import ollama
def generate_final_answer(state:AgentState,model:str="llama3.2")->str:

    print("---------------------",state.get_next_pending_task())

    prompt=f"""
    You are the Final Answer Generator for AI Agent
    ALL planned subtasks are executed
    Generate a clear response answering uses orginal goal
    Orignal goal : {state.user_goal}
    {state.get_next_pending_task}
    """


    response = ollama.chat(
        model=model,
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]

    )


    return response["message"]["content"]


