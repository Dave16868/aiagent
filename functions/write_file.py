import os 

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