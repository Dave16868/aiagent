import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import function_call, available_functions
from prompts import system_prompt
from functions.config import MAX_ITER

def main():
    # Load Env variable
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # compile prompt(s)
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    # check presence of prompt
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    prompt = " ".join(args)

    # verbose flag
    verbose = "--verbose" in sys.argv
    if verbose:
        print(f"User prompt: {prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITER:
            print(f"Maximum iterations ({MAX_ITER}) reached.")
            sys.exit(1)
        
        try: 
            response_text = generate_content(client, messages, verbose)
            if response_text: # if no text it will be none
                print("Final Response:")
                print(response_text)
                break
        except Exception as e:
            print(f"Error during content generation loop: {e}")
    
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

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    # when model wants to call function, call function and append messages with type.Content
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

    messages.append(types.Content(role="tool", parts=function_responses))
    


if __name__ == "__main__":  
    main()
