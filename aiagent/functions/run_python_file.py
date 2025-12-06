import os
import subprocess

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file, returning its stdout, stderr, and exit code (if non-zero), or an error.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,  
                items=types.Schema(type=types.Type.STRING),
                description="A list of arguments to be run on the Python file.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_filepath = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_filepath.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if os.path.exists(abs_filepath) == False:
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    
    cmd = ["python", abs_filepath] + args
    try:
        completed = subprocess.run(
            cmd, 
            timeout=30, 
            capture_output=True,
            text=True,
            cwd= abs_working_dir,
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"

    if not completed.stdout and not completed.stderr:
        return "No output produced"
    
    completed_string = (f"STDOUT: {completed.stdout}\nSTDERR: {completed.stderr}")

    if completed.returncode != 0:
        return completed_string + f"\nProcess exited with code {completed.returncode}"
    
    return completed_string
