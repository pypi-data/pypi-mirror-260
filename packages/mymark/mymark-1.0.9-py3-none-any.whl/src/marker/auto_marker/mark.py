import subprocess

def mark_code(mark_scheme_file_path, code_directory):
    # Define the command to mark the code.
    mark_code_command = f"python3 mark.py {mark_scheme_file_path} {code_directory}"

    # Execute the command.
    subprocess.run(mark_code_command, shell=True)
