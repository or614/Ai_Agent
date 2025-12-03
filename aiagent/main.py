import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

args = parser.parse_args()
messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]

client = genai.Client(api_key=api_key)
ai_model = "gemini-2.5-flash"

response = client.models.generate_content(model="gemini-2.5-flash", contents=messages)
if response.usage_metadata != None:
    if args.verbose == True:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        print(f"User prompt: {args.prompt}\nPrompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}\nResponse: \n{response.text}")
    else:
        print(response.text)
