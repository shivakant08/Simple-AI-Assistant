# Previous version (kept for comparison):
import os

from openai import OpenAI
from dotenv import load_dotenv

from tools import TOOLS,  run_tool
from utilities.utilities import log


load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

messages= []

MAX_STEPS= 5

messages.append(
    {
        "role": "system",
        "content":"Act like a smart and humble person and respond within 50 words.",
    }
)

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
    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages,
        tools=TOOLS
    )

        msg = response.choices[0].message

        if not msg.tool_calls:
            break

        log(f"Step {step+1}: Model Requested {len(msg.tool_calls)} tooll calls")

        messages.append(msg)

        for tool_call in msg.tool_calls:
            result = run_tool(tool_call)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                }
            )

    else:
        fallback = "Sorry, I could not finish this within the steps limit."
        messages.append(
            {
                "role": "assistant",
                "content": fallback
            }
        )
        print("Assistant: " + fallback)
        continue



    messages.append(
        {
        "role": "assistant",
        "content": msg.content
        }
    )

    print("Assistant: " + (msg.content or ""))

# Fixed version:
# from openai import OpenAI
# from dotenv import load_dotenv
# from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP
# import os
# import json

# load_dotenv()

# client = OpenAI(
#     base_url=os.getenv("BASE_URL"),
#     api_key=os.getenv("API_KEY")
# )

# messages = [
#     {
#         "role": "system",
#         "content": "Act like a funny but serious person and respond within 20 words.",
#     }
# ]

# while True:
#     user_input = input("\nShivakant: ")

#     if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
#         break

#     messages.append(
#         {
#             "role": "user",
#             "content": user_input
#         }
#     )
#     while True:
#         response = client.chat.completions.create(
#             model=os.getenv("MODEL"),
#             messages=messages,
#             tools=TOOLS,
#         )
#         msg = response.choices[0].message

#         if not msg.tool_calls:
#             answer = msg.content or ""
#             messages.append({"role": "assistant", "content": answer})
#             print(f"Assistant: {answer}")
#             break

#         messages.append(msg.model_dump(exclude_none=True))
#         for tool_call in msg.tool_calls:
#             func_name = tool_call.function.name
#             func_args = json.loads(tool_call.function.arguments or "{}")
#             fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
#             result = fn(**func_args)

#             messages.append(
#                 {
#                     "role": "tool",
#                     "tool_call_id": tool_call.id,
#                     "content": str(result),
#                 }
#             )