import asyncio
from contextlib import AsyncExitStack
from mcp.client.stdio import stdio_client,StdioServerParameters
from mcp.client.session import ClientSession
import ollama
import json
from agentstate import AgentState
from decomposer import decompose_plan
from generate import generate_final_answer
from planner import execute_subtask_with_mcp


async def run_mcp_agent():
    #define how to launch mcp server process
    server_param = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with AsyncExitStack() as exit_stack:
        #connect to mcp server
        read,write = await exit_stack.enter_async_context(stdio_client(server_param))
        session = await exit_stack.enter_async_context(ClientSession(read,write))


        await session.initialize()


        response = await session.list_tools()

        available_tools = [
            {
                "type":"function",
                "function":{
                    "name":t.name,
                    "description":t.description,
                    "parameters":t.inputSchema
                }
            }
            for t in response.tools
        ]


        user_goal = (
            "read app.log to see how many MB of dump file created"\
            "check our current free dsik space and calculate what percentage" \
            "of our free disk place those file are present"
        )

        state = AgentState(user_goal)

        list_tools = []

        for tool in response.tools:
            list_tools.append(tool.name)

        tasks = decompose_plan(user_goal,list_tools)

        state.set_tasks(tasks=tasks)

        print("Generated Tasks:", tasks)



        while(next_task:=state.get_next_pending_task()) is not None:
            print("Executing Task...",next_task.description)
            await execute_subtask_with_mcp(
                session=session,
                current_task=next_task,
                state=state,
                ollama_tools=available_tools,
                model="llama3.2"
            )

           



        final_answer = generate_final_answer(state)


        print("------------",final_answer)


if __name__ == "__main__":
    asyncio.run(run_mcp_agent())
