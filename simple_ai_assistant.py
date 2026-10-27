# Previous version (kept for comparison):
# from openai import OpenAI
# from dotenv import load_dotenv
# from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP
# import os
# import json
#
# load_dotenv()
#
# client = OpenAI(
#     base_url=os.getenv("BASE_URL"),
#     api_key=os.getenv("API_KEY")
# )
#
# messages= []
# messages.append(
#     {
#         "role": "system",
#         "content":"Act like a funny but serious person and respond within 20 words.",
#     }
# )
#
# while True:
#     user_input = input("\nShivakant: ")
#
#     if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
#         break
#
#     messages.append(
#         {
#             "role": "user",
#             "content": user_input
#         }
#     )
#     response = client.chat.completions.create(
#         model=os.getenv("MODEL"),
#         messages=messages,
#         tools=TOOLS
#     )
#
#     msg = response.choices[0].message
#     if msg.tool_calls:
#         messages.append(msg)
#
#     for tool_call in msg.tool_calls:
#         func_name = tool_call.function.name
#         func_args = json.loads(tool_call.function.arguments or "{}")
#
#         fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
#         result = fn(**func_args)
#
#         messages.append(
#             {
#                 "role": "tool",
#                 "tool_id": tool_call.id,
#                 "content": str(result)
#             }
#         )
#
#     response = client.chat.completions.create(
#         model=os.getenv("MODEL"),
#         messages=messages
#     )
#
#     msg = response.choices[0].message
#
# messages.append(
#     {
#         "role": "assistant",
#         "content": msg.content
#     }
# )
#
# print("Assistant" + msg.content)

# Fixed version:
from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP
import os
import json

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

messages = [
    {
        "role": "system",
        "content": "Act like a funny but serious person and respond within 20 words.",
    }
]

while True:
    user_input = input("\nShivakant: ")

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        break

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    while True:
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            tools=TOOLS,
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            answer = msg.content or ""
            messages.append({"role": "assistant", "content": answer})
            print(f"Assistant: {answer}")
            break

        messages.append(msg.model_dump(exclude_none=True))
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments or "{}")
            fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
            result = fn(**func_args)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )