import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))

    if target_dir.startswith(abs_working_dir) == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if os.path.isdir(target_dir) == False:
        return f'Error: "{directory}" is not a directory'
    
    dir_contents = os.listdir(target_dir)

    new_contents = []
    for file in dir_contents:
        try:
            filesize = os.path.getsize(target_dir+"/"+file)
        except:
            return "Error: Filesize not working"
        try:
            is_dir = not os.path.isfile(target_dir+"/"+file)
        except:
            return "Error: IsFile not working"
        new_contents.append(f"- {file}: file_size={filesize} bytes, is_dir={is_dir}")

    contents_string = "\n".join(new_contents)
    return contents_string



