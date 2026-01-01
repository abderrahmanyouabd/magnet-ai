import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import argparse
import sys

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model_name = os.getenv("GEMINI_MODEL")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", "-p", type=str, required=True)
    parser.add_argument("--verbose", "-v", action="store_true", default=False)
    args = parser.parse_args()
    try:
        messages = [
            types.Content(role="user", parts=[types.Part(text=args.prompt)])
        ]
        response = client.models.generate_content(model=model_name, contents=messages)
        if args.verbose:
            print(response)
        else:
            print(response.text)
    except Exception as e:
        print(e)
    finally:
        sys.exit(0)
