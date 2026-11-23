import os
import csv
import json
import asyncio
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.session import ClientSession
from contextlib import AsyncExitStack
from tools.state import AgentState
from AgentStateClass.decomposer import decompose_plan
from StructuredOutput.planner import execute_subtask_with_mcp
from Executor.generator import generate_final_answer


def create_sample_files():
    expenses = [
        ["Date", "Category", "Amount", "Description"],
        ["20/11/2026", "Food", 1000, "Pizza"],
        ["21/11/2026", "Utilities", 300, "Recharge"],
        ["22/11/2026", "Entertainment", 400, "Movie"],
        ["22/11/2026", "Food", 500, "Pav bhaji"],
    ]

    expenses_path = os.path.join(PROJECT_DIR, "expenses.csv")
    with open(expenses_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(expenses)

    budgets = {
        "Food": 200,
        "Utilities": 500,
        "Entertainment": 100,
    }

    budget_path = os.path.join(PROJECT_DIR, "budget.json")
    with open(budget_path, "w") as file:
        json.dump(budgets, file, indent=4)


async def run_mcp_agent():
    server_param = StdioServerParameters(
        command=sys.executable,
        args=[os.path.join(PROJECT_DIR, "server.py")],
    )

    async with AsyncExitStack() as exit_stack:
        read, write = await exit_stack.enter_async_context(stdio_client(server_param))
        session = await exit_stack.enter_async_context(ClientSession(read, write))

        await session.initialize()
        response = await session.list_tools()

        available_tools = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.inputSchema,
                },
            }
            for t in response.tools
        ]

        user_goal = (
            "Read 'expenses.csv' to find the total amount spent on 'Food', "
            "check our 'Food' budget limit from 'budget.json', calculate the "
            "exact dollar difference (or overage), and generate a brief budget "
            "status summary."
        )

        state = AgentState(user_goal=user_goal)
        tasks = decompose_plan(available_tools=available_tools, user_goal=user_goal)
        state.set_tasks(tasks=tasks)
        state.display_board()

        while (next_task := state.get_next_pending_task()) is not None:
            print("Executing Task...", next_task.description)
            await execute_subtask_with_mcp(
                session=session,
                current_task=next_task,
                state=state,
                ollama_tools=available_tools,
            )
            state.display_board()

        final_answer = generate_final_answer(state)
        print("------------>", final_answer)


if __name__ == "__main__":
    create_sample_files()
    asyncio.run(run_mcp_agent())
