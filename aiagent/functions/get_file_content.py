import os
from google import genai
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the file contents, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file, relative to the working directory",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_filepath = os.path.abspath(file_path)
    abs_filepath = os.path.abspath(os.path.join(working_directory, file_path))

    if abs_filepath.startswith(abs_working_dir) == False:
        return f'Error: Cannot list "{abs_filepath}" as it is outside the permitted working directory'

    if os.path.isfile(abs_filepath) == False:
        return f'Error: File not found or is not a regular file: "{abs_filepath}"'
    try:
        with open(abs_filepath) as f:
            contents = f.read()
    except:
        return f"Error: could not open/read file at filepath {abs_filepath}"
    if len(contents) > 10000:
        return f'{contents[:1000]}[...File "{file_path}" truncated at 10000 characters]'

    return contents
    