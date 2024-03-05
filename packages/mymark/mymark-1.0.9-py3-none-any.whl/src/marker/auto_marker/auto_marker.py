import os
import sys
import requests
from mark import mark_code

def main(code_directory):
    # Fetch environment variables.
    module_name = os.environ.get("MODULE_NAME")
    api_key = os.environ.get("API_KEY")

    # Make request to server to fetch mark scheme.
    server_url = "https://146.169.43.198:8080/"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"module_name": module_name}
    response = requests.get(f"{server_url}/mark_scheme", 
                            params=params, 
                            headers=headers)

    # Check if request was successful.
    if response.status_code == 200:
        # Get the mark scheme content.
        mark_scheme_content = response.text

        # Define the file path for the new file.
        mark_scheme_file_path = "mark_scheme.ms"

        # Write the mark scheme content to the new file.
        with open(mark_scheme_file_path, "w") as mark_scheme_file:
            mark_scheme_file.write(mark_scheme_content)

        print(f"Mark scheme successfully saved to {mark_scheme_file_path}")

        # Run the marking function in mark.py.
        mark_code(mark_scheme_file_path, code_directory)
    else:
        print(f"Failed to fetch mark scheme: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print("I am running!")

    if len(sys.argv) != 2:
        print("Usage: auto-marker <path_to_code_directory>")
        sys.exit(1)
        
    code_directory = sys.argv[1]
    main(code_directory)
