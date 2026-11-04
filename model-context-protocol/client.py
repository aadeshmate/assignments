import asyncio
from contextlib import AsyncExitStack
from mcp.client.stdio import stdio_client,StdioServerParameters
from mcp.client.session import ClientSession
import ollama
import json

async def run_mcp_agent():
    #define how to launch mcp server process

    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with AsyncExitStack() as exit_stack:
        #connect to mcp server
        read,write = await exit_stack.enter_async_context(stdio_client(server_params))

        session = await exit_stack.enter_async_context(ClientSession(read,write))

        await session.initialize()

        response = await session.list_tools()

        available_tools = [
            {
                "type":"function",
                "function" : {
                    "name" : tool.name,
                    "description":"",
                    "parameters":tool.inputSchema
                }
            } for tool in response.tools
        ]

        messages = [
            {
                "role":"system",
                "content":""
            }
        ]


        user_input = input("Enter : ")
        messages.append(
            {
                "role":"user",
                "content":user_input
            }
        )


        ai_response = ollama.chat(
            model='qwen3:4b',
            messages=messages,
            tools=available_tools
        )

        print(ai_response["message"].model_dump_json(indent=4))

        if ai_response.get("message",{}).get("tool_calls"):
            for tool_call in ai_response["message"]["tool_calls"]:
                function_name = tool_call["function"]["name"]
                function_args = tool_call["function"]["arguments"]

                tool_result = await session.call_tool(function_name,arguments=function_args)

                

                raw_output = tool_result.content[0].text


                messages.append(ai_response['message'])

                messages.append({
                    "role":"tool",
                    "content":raw_output
                })


                final_response = ollama.chat(
                    model="qwen3:4b",
                    messages=messages
                )

                print(json.dumps(final_response["message"].model_dump(),indent=4))


if __name__ == "__main__":
    asyncio.run(run_mcp_agent())

                
