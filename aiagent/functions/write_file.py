import os
from google import genai
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to write to a file, it will override the contents of the current file",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_filepath = os.path.abspath(os.path.join(working_directory, file_path))

    if abs_filepath.startswith(abs_working_dir) == False:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_filepath):
        try:
            dir_name = os.path.dirname(abs_filepath)
            os.makedirs(dir_name, exist_ok=True)
        except:
            return f"Error: Cannot make filepath for filepath {abs_filepath}"
    
    with open(abs_filepath, "w") as f:
        f.write(content)
    
    return f'Successfully wrote to "{abs_filepath}" ({len(content)} characters written)'
        