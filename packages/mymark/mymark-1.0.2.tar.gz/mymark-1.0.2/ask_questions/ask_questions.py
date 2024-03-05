import os
import sys
import warnings
from typing import Any

import requests
from urllib3.exceptions import InsecureRequestWarning

# Suppress InsecureRequestWarning
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

JsonBlob = dict[str, Any]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_script.py <code_folder>")
        sys.exit(1)

    code_folder = sys.argv[1]
    all_code = []
    for root, _, files in os.walk(code_folder):
        for file in files:
            if file.endswith(".java"):
                with open(os.path.join(root, file), "r") as f:
                    all_code.append(f.read())

    server_address = f"https://{os.getenv('SERVER_HOST')}:{os.getenv('SERVER_PORT_HTTPS')}"

    context: list[JsonBlob] = []
    while question := input("Enter question: "):
        context.append({"role": "user", "content": question})
        answer = requests.post(
            f"{server_address}/modules/SED/exercises/exercise_4/autota/ask",
            json={
                "code": "\n\n\n".join(all_code),
                "context": context,
            },
            headers={
                "Content-Type": "application/json",
            },
            timeout=5,
            verify=False,
        ).json()["answer"]
        print(answer)
        context.append({"role": "assistant", "content": answer})
