import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import function_call, available_functions
from prompts import system_prompt

def main():
    # Load Env variable
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # check presence of prompt
    if len(sys.argv) < 2:
        print("Error: please provide a prompt")
        sys.exit(1)

    # compile prompt(s)
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    prompt = " ".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    # verbose flag
    verbose = "--verbose" in sys.argv
    if verbose:
        print(f"User prompt: {prompt}")

    generate_content(client, messages, verbose)
    
def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
        )
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        return response.text

    function_responses = []
    for call in response.function_calls:
        call_result = function_call(call, verbose)
        if not call_result.parts or not call_result.parts[0].function_response.response:
            raise Exception("Fatal Error: empty function call result.")
        if verbose:
            print(f"-> {call_result.parts[0].function_response.response}")
        function_responses.append(call_result.parts[0])
    
    if not function_responses:
        raise Exception("no function responses generated, exiting.")


if __name__ == "__main__":  
    main()
