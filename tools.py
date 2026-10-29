from datetime import datetime
import requests
import json
import wikipedia
from utilities.utilities import log


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_city_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    result = requests.get(url, timeout= 20)
    result.raise_for_status()
    return result.text

def get_my_city():
    return "Mumbai"

# def wikipedia_search(query):
#     try:
#         wikipedia.set_lang("en")
#         summary = wikipedia.summary(query, sentences = 3)
#         return {
#             "topic": query,
#             "summary": summary
#         }
#     except wikipedia.exceptions.DisambiguationError as e:
#         return {
#             "error": "Multiple results found",
#             "options":e.options[:5]
#         }
#     except wikipedia.exceptions.PageError:
#         return {
#             "error": f"No Wikipedia page found for '{query}'"
#         }
#     except Exception as e:
#         return {
#             "error": str(e)
#         }

def wikipedia_search(query):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url , timeout=20)

    if response.status_code ==200:
        data = response.json()
        return data.get("extract", "No summary found")
    return "Tpic not found"


TOOLS = [
    {
        "type": "function",
        "function":{
            "name": "get_current_time",
            "description": "Returns the current date and time as a formatted string.",
            "parameters":{
                "type": "object",
                "properties":{}
                }
            }
        },
        {
            "type": "function",
            "function":{
                "name": "get_city_weather",
                "description": "Return the weather of a given city.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "city":{
                            "type": "string",
                            "description": "City to get the weather for."
                        }
                    },
                    "required": ["city"]
                }
            }
        },


        {
            "type": "function",
            "function":{
                "name": "wikipedia_search",
                "description": "Search Wikipedia and return a summary about the topic.",
                "parameters":{
                    "type": "object",
                    "properties":{
                        "query":{
                            "type":"string",
                            "description":"Topic to search on Wikipedia"
                        }
                    },
                    "required":["query"]
                }
            }
        },
        {
                "type": "function",
                "function":{
                    "name": "get_my_city",
                    "description": "Returns the city.Use it whenever the user says words like 'My City', 'My Location', 'My Home'",
                    "parameters":{
                        "type": "object",
                        "properties":{}
                        }
                    }
                },
    
]

FUNCTION_NAME_TO_FUNCTION_MAP={
    "get_current_time": get_current_time,
    "get_city_weather": get_city_weather,
    "wikipedia_search": wikipedia_search,
    "get_my_city": get_my_city
}

def run_tool(tool_call):
    func_name = tool_call.function.name
    func_args = {}
    
    try:
        func_args = json.loads(tool_call.function.arguments or "{}")
        log(f"{func_name}({func_args})")
        fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
        result = fn(**func_args)
    except Exception as e:
        result = f"Error while running the {func_name}: {e}"
    
    log(f"  {result}")
    return str(result)