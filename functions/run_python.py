import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    path = os.path.join(working_directory, file_path)
    abspath = os.path.abspath(path)
    if not abspath.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abspath):
        return f'Error: File "{file_path}" not found.'
    if not abspath.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try: 
        arglist = ["python3", abspath]
        for arg in args: # instead of for loop, could also use a if statement to check for args, then use arglist.extend 
            arglist.append(arg)

        CompletedProcess = subprocess.run(arglist, timeout=30, capture_output=True, cwd=os.path.abspath(working_directory), text=True)

        output = []

        if CompletedProcess.stdout:
            stdout = "STDOUT:" + "\n" + CompletedProcess.stdout
            output.append(stdout)
        if CompletedProcess.stderr:
            stderr = "STDERR:" + "\n" + CompletedProcess.stderr
            output.append(stderr)
        if CompletedProcess.returncode != 0:
            output.append(f'Process exited with code {CompletedProcess.returncode}')
        
        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f'Error: executing Python file: {e}'