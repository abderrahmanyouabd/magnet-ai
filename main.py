import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import argparse
import sys
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from config import SYSTEM_PROMPT
from functions.schemas import schema_get_files_info

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model_name = os.getenv("GEMINI_MODEL")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", "-p", type=str, required=True)
    parser.add_argument("--verbose", "-v", action="store_true", default=False)
    args = parser.parse_args()
    try:
        messages = [
            types.Content(role="user", parts=[types.Part(text=args.prompt)])
        ]

        available_functions = types.Tool(
            function_declarations=[
                schema_get_files_info,
            ]
        )

        config = types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT,
        )

        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=config,
        )

        if response.function_calls:
            for function_call_part in response.function_calls:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                if function_call_part.name == "get_files_info":
                    # Extract args with defaults
                    working_dir = function_call_part.args.get('working_dir', '.')
                    dir_path = function_call_part.args.get('dir', '.')
                    result = get_files_info(working_dir, dir_path)
                    print(result)
        else:
            if args.verbose:
                print(response)
            else:
                print(response.text)
    except Exception as e:
        print(e)
    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()

    # print(run_python_file("example_project_calculator", "main.py", interactive=True))
