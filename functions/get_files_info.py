import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    path = os.path.join(working_directory, directory)
    abspath = os.path.abspath(path)
    if not abspath.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory' # errors in functions returned as strings not raised so that LLMs can handle gracefully
    if not os.path.isdir(abspath):
        return f'Error: "{directory}" is not a directory'
    try: # good practice to use try axcept statements to divide and except blocks of code for ease of debugging
        dir_list = os.listdir(abspath)
        str_content = []
        for item in dir_list:
            item_path = os.path.join(abspath, item)
            str_content.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")
        result = "\n".join(str_content)
        return result
    except Exception as e:
        return f"Error listing files: {e}"

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


