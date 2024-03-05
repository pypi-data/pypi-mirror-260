import os
import sys
from src.adapter.adapter_gpt import GPTRequest, GPTModel, GPTRole, GPTAdapter


def get_hint(question: str, code_folder: str) -> str:
    """
    Generate a hint based on the student's question and the code in the
    specified folder.
    """
    # Variable to store the context.
    context = ""

    exercise_description = (
        "In this exercise the student has been asked to implement the builder "
        "design pattern in java for the BookSearchQuery class. "
        "They also have to introduce the singleton "
        "pattern for the code for BritishLibraryCatalogue to ensure that there "
        "is only ever one instance created. They then have to refactor the code"
        " to follow the principle of dependency inversion so that the "
        "dependency on the concrete class is broken. Finally the student has to"
        " change the unit test for the BookSearchQuery to use mock or fake "
        "objects."
    )

    # Concatenate all code files under the code folder.
    all_code = ""
    for root, _, files in os.walk(code_folder):
        for file in files:
            if file.endswith(".java"):
                with open(os.path.join(root, file), "r") as f:
                    all_code += f.read() + "\n"

    hint = ""
    # Create a GPTRequest object.
    request = GPTRequest(
        query=(
            exercise_description
            + "\n\n"
            + context
            + "\n\nStudent's question: "
            + question
            + "\n\nCode:\n"
            + all_code
            + "\nProvide guidance, only answering the student's question"
            + " and giving no extra information. "
            + "Do not provide complete solutions. Do not provide code examples."
        ),
        role=GPTRole.USER,
        model=GPTModel.GPT4LATEST,
        temperature=0.7,
    )

    # Create a GPTAdapter instance.
    adapter = GPTAdapter()
    print("request sent")

    # Get the response (hint to question) using the adapter.
    hint = adapter.get_response(request)

    # Update the context with the latest response.
    context += "\n\n" + question + "\n" + hint

    return hint


def ask(question: str, code_folder: str) -> None:
    """
    Process the student's question and print the hint.
    """

    hint = get_hint(question, code_folder)
    print(hint)


def main_func() -> None:
    if len(sys.argv) != 3:
        print("Usage: python your_script.py <question> <code_folder>")
        sys.exit(1)

    question = sys.argv[1]
    code_folder = sys.argv[2]

    ask(question, code_folder)
