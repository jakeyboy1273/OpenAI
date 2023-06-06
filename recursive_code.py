import os
import openai
import subprocess
import sys

# Configure the OpenAI API
# TODO: make this a .env file instead of pasting it directly into here
openai.api_key = ("KEY GOES HERE")

def get_code_from_openai_turbo(prompt):
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages = [{
            "role": "system",
            "content" : "You are a competent python programmer. You specialise in writing clean, efficient code. When prompted to write or correct code, you are instructed to only respond with the code only, and no other text whatsoever outside of the python code."
            },
            {
                "role": "user",
                "content" : prompt
                },
        ]
    )
    response_code = response["choices"][0]["message"]["content"].strip()
    return response_code

def get_code_from_openai(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        # engine = "gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    response_code = response.choices[0].text.strip()
    # TODO: use debug.logging for this and format it better
    # print(f"ChatGPT request:\n{prompt}\n\n{response_code}")
    return response_code

def execute_code(code, destination="temp_code.py", timeout=10):
    """Write the code input to the destination file and attempt to run it"""

    # Open the destination and write the code to it
    with open(destination, "w") as f:
        f.write(code)

    try:
        # Run the new code and return the output
        result = subprocess.run([sys.executable, "temp_code.py"], capture_output=True, text=True, check=True, timeout=timeout)
        return result.stdout, False
    except subprocess.CalledProcessError as e:
        # If an error occurs, return the output and the error code
        print(e.stderr)
        return e.stdout + e.stderr, True
    except subprocess.TimeoutExpired:
        # If a timeout occurs, return the timeout message
        return "Execution timed out.", True

def request_new_feature(code):
    prompt = f"The following Python code is working without errors:\n\n{code}\n\n Please generate a brand new feature that is different from the existing code and provide the Python code for it. Write a concise feature scope in comments before the new code."
    new_feature_code = get_code_from_openai(prompt)
    return new_feature_code

def code_writing_loop(idea, iterations):
    i = 0
    prompt = idea
    while i < iterations:   
        error_exists = True
        while error_exists:
            print("Generating code using OpenAI API...")
            # Generate code using OpenAI API
            code = get_code_from_openai(prompt)
            print("Executing the code and checking for errors...")

            # Execute the code and capture the output
            output, error_exists = execute_code(code)
            if error_exists:
                print("Errors found, sending output to GPT for fixing...")
                # Send the output to GPT to fix the errors
                prompt = f"The following Python code has some errors:\n\n{code}\n\nError message:\n{output}\n\nPlease fix the errors and provide the corrected code."
        while not error_exists:
            i += 1
            print("No errors found. Requesting a new feature...")
            # When there are no errors, ask GPT to suggest a new feature
            new_feature = request_new_feature(code)
            print("Adding new feature to the code and checking for errors...")

            # Add the new feature to the code and check for errors again
            code += "\n\n" + new_feature
            output, error_exists = execute_code(code)
            if error_exists:
                print("Errors found in the new feature, sending output to GPT for fixing...")
                # Send the output to GPT to fix the errors in the new feature
                prompt = f"The following Python code has some errors after adding the new feature:\n\n{code}\n\nError message:\n{output}\n\nPlease fix the errors and provide the corrected code."

def main():
    idea = "Write python code for a simple game of snake using pygame."
    code_writing_loop(idea, 5)

if __name__ == "__main__":
    main()