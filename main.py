import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import argparse
import sys
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from config import SYSTEM_PROMPT
from functions.schemas import schema_get_files_info, schema_write_file, schema_run_python_file, schema_get_file_content

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model_name = os.getenv("GEMINI_MODEL")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", "-p", type=str, required=True)
    parser.add_argument("--verbose", "-v", action="store_true", default=False)
    parser.add_argument("--max-turns", type=int, default=4, help="Maximum number of function calling turns")
    args = parser.parse_args()
    
    try:
        messages = [
            types.Content(role="user", parts=[types.Part(text=args.prompt)])
        ]

        available_functions = types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_get_file_content,
                schema_write_file,
                schema_run_python_file,
            ]
        )

        config = types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT,
        )

        # Agentic loop: Keep calling functions until AI gives final answer
        for turn in range(args.max_turns):
            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=config,
            )

            # Check if AI wants to call functions
            if response.function_calls:
                if args.verbose:
                    print(f"\n--- Turn {turn + 1}: AI wants to call {len(response.function_calls)} function(s) ---")
                
                # Add AI's response (with function calls) to conversation
                messages.append(types.Content(
                    role="model",
                    parts=[types.Part(function_call=fc) for fc in response.function_calls]
                ))
                
                # Execute each function call
                function_responses = []
                for function_call_part in response.function_calls:
                    if args.verbose:
                        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                    
                    # Route to appropriate function
                    if function_call_part.name == "get_files_info":
                        working_dir = function_call_part.args.get('working_dir', '.')
                        dir_path = function_call_part.args.get('dir', '.')
                        result = get_files_info(working_dir, dir_path)
                        
                    elif function_call_part.name == "get_file_content":
                        working_dir = function_call_part.args.get('work_dir', '.')
                        file_path = function_call_part.args.get('file_path', '')
                        result = get_file_content(working_dir, file_path)
                        
                    elif function_call_part.name == "write_file":
                        working_dir = function_call_part.args.get('work_dir', '.')
                        file_path = function_call_part.args.get('file_path', '')
                        content = function_call_part.args.get('content', '')
                        target_content = function_call_part.args.get('target_content', None)
                        start_line = function_call_part.args.get('start_line', None)
                        end_line = function_call_part.args.get('end_line', None)
                        result = write_file(working_dir, file_path, content, target_content, start_line, end_line)

                    elif function_call_part.name == "run_python_file":
                        working_dir = function_call_part.args.get('work_dir', '.')
                        file_path = function_call_part.args.get('file_path', '')
                        timeout = function_call_part.args.get('timeout', 30)
                        interactive = function_call_part.args.get('interactive', False)
                        cli_args = function_call_part.args.get('cli_args', None)
                        result = run_python_file(working_dir, file_path, timeout, interactive, cli_args)
                        
                    else:
                        result = f"Error: Unknown function call: {function_call_part.name}"
                    
                    if args.verbose:
                        print(f"Function result:\n{result}\n")
                    
                    # Add function response
                    function_responses.append(
                        types.Part(function_response=types.FunctionResponse(
                            name=function_call_part.name,
                            response={"result": result}
                        ))
                    )
                
                # Add function results to conversation
                messages.append(types.Content(
                    role="user",
                    parts=function_responses
                ))
                
                # Loop continues - AI will decide what to do next
                
            else:
                # No function calls - AI has final answer
                if args.verbose:
                    print(f"\n--- Turn {turn + 1}: AI provided final answer ---")
                print(response.text)
                break
        else:
            # Max turns reached
            print(f"Warning: Reached maximum number of turns ({args.max_turns})")
            if response.text:
                print(response.text)
                
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()

    # print(run_python_file("example_project_calculator", "main.py", interactive=True))
