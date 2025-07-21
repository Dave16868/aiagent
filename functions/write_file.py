import os 
from google.genai import types

def write_file(working_directory, file_path, content):
    path = os.path.join(working_directory, file_path)
    abspath = os.path.abspath(path)
    if not abspath.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory' # errors in functions returned as strings not raised so that LLMs can handle gracefully
    if not os.path.exists(os.path.dirname(abspath)):
        try:
            os.makedirs(abspath)
        except Exception as e:
            return f'Error creating directory for {file_path}: {e}'
    try:
        with open(abspath, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing into file: {e}'
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes/rewrites the file provided by the file path relative to the working directory with the content provided as a string. Creates the file if it doesn't exists.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path":types.Schema(
                type=types.Type.STRING,
                description="the path to the file that is written into. Must be within working directory.",
            ),
            "content":types.Schema(
                type=types.Type.STRING,
                description="The string that is written into the file designated by the filepath.",
            ),
        },
        required=["file_path", "content"],
    ),
)