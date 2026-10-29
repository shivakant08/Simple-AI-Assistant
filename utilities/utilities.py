# import os
# from colorama import init, Fore, Style

# init()

# def log(text):
#     if os.getenv("DEBUG") == "True":
#         print(f"  {START_SEQUENCE}{text}{END_SEQUENCE}")

import os
from colorama import init, Fore, Style

init()  # Enables ANSI support on Windows

def log(text):
    if os.getenv("DEBUG", "").strip().lower() == "true":
        print(f"{Fore.RED}{text}{Style.RESET_ALL}")