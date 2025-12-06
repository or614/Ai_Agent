import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_files_content import schema_get_files_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

args = parser.parse_args()
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

client = genai.Client(api_key=api_key)
ai_model = "gemini-2.5-flash"

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file],
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages, 
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ),
    )

if response.usage_metadata != None:
    if args.verbose == True:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        print(f"User prompt: {args.prompt}\nPrompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}\nResponse: \n{response.text}")
    else:
        print(response.text)
    
    if response.function_calls != None:
        for function in response.function_calls:
            print(f"Calling function: {function.name}({function.args})")
        else:
            print(response.text)

