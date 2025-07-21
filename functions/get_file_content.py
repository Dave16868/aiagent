import os
from functions.config import MAX_CHAR
from google.genai import types

def get_file_content(working_directory, file_path):
    path = os.path.join(working_directory, file_path)
    abspath = os.path.abspath(path)
    if not abspath.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abspath):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abspath, "r") as f:
            content_string = f.read(MAX_CHAR)
        return content_string
    except Exception as e:
        return f"Error reading file: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a specified file. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file that is read, relative to the working directory. Will not read directories or files outside the working directory.",
            ),
        },
    ),
)