import os
from google import genai
from dotenv import load_dotenv
import json
import argparse


load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model_name = os.getenv("GEMINI_MODEL")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", "-p", type=str, required=True)
    args = parser.parse_args()
    response = client.models.generate_content(model=model_name, contents=args.prompt)
    print(response.text)