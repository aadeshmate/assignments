import ollama
import json
from react_tool import AVAILABLE_TOOL,TOOL_REGISTRY

def run_cli_agent():
    messages = [{"role" : "system","content" : "your are an CLI agentt"}]
    while True:
        user_input = input("Enter string : ")
        messages.append(
            {
                "role" : "user",
                "content" : user_input
            }
        )

        response = ollama.chat(
            model='qwen3:4b',
            messages=messages,
            tools=AVAILABLE_TOOL
        )

        print(json.dumps(response.model_dump(), indent=4))

        if response.get('message',{}).get('tool_calls'):
            tool_calls = response['message']['tool_calls']
            messages.append(response["message"])
            for tool in tool_calls:
                function_name = tool['function']['name']
                arguments = tool['function']['arguments']

                function_tool_call = TOOL_REGISTRY.get(function_name)

                if function_tool_call:
                    raw_result = function_tool_call(**arguments)
                    messages.append({
                        "role" : "tool",
                        "content" : raw_result,
                        "name" : function_name
                    })

                print(function_tool_call,"\n\n",raw_result)
                result = ollama.chat(
                    model='qwen3:4b',
                    messages=messages
                )

                print(json.dumps(result.model_dump(), indent=4))


if __name__ == "__main__":
    run_cli_agent()





