import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"

    function_map = {
        "get_file_content":get_file_content,
        "get_files_info":get_files_info,
        "run_python_file":run_python_file,
        "write_file":write_file,
    }

    if function_call_part.name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    
    func = function_map[function_call_part.name]
    function_result = (func(**args))

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )

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

counter = 20
for _ in range(20):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages, 
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
        )

    if response.text != None and response.function_calls == None:
        print("Final response:")
        print(response.text)
        break


    for candidate in response.candidates:
        messages.append(candidate.content)


        
    if response.function_calls != None:
        func_list = []
        for function in response.function_calls:
            print(f"Calling function: {function.name}({function.args})")
            function_result = call_function(function, args.verbose)
            try:
                result_response = function_result.parts[0].function_response.response
            except Exception as e:
                raise Exception(f"Fatal Error: {e}")
            func_list.append(function_result.parts[0])
            if args.verbose == True:
                print(f"-> {function_result.parts[0].function_response.response}")
        
        messages.append(
        types.Content(
            role="user",
            parts=func_list,
        )
    )
    
    if response.text and not response.function_calls:
        print("Final response:")
        print(response.text)
        break