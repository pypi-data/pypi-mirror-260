import sys
import os

from marker.command_line_tool.utils import write_json_to_file, write_to_file
from marker.marker.interpreter import Interpreter

def main(mark_scheme_path: (str | None)) -> None:
    # Check for correct number of arguments.
    if len(sys.argv) != 2:
        raise ValueError(
            f"Insufficient arguments! Expected 2 arguments but got {len(sys.argv) - 1}"
        )

    # Mark code and write feedback.
    interpreter = Interpreter(mark_scheme_path, sys.argv[1], debug_mode=True)
    interpreter.run()

    marks = interpreter.get_marks()
    feedback = interpreter.get_feedback()

    write_to_file("./comments.txt", "\n\n".join(feedback))
    write_json_to_file("./marks.json", marks)

    interpreter.print_warnings()

if __name__ == "__main__":
    main(os.getenv('EXERCISE_NAME'))
