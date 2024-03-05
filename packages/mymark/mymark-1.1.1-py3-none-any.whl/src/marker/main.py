import sys

from src.command_line_tool.utils import write_json_to_file, write_to_file
from src.marker.interpreter import Interpreter


def main_func() -> None:
    """Extracts the specification and code files, calls the LLM on it and
    outputs the response"""
    if len(sys.argv) == 1:  # For debugger
        sys.argv.append(".\\mark_schemes\\exercise_4.ms")
        sys.argv.append(".\\user_files\\SED_example\\code\\")
    if len(sys.argv) != 3:
        raise ValueError(
            f"Insufficient arguments! Expected 2 arguments but got {len(sys.argv) - 1}"
        )
    interpreter = Interpreter(sys.argv[1], sys.argv[2], debug_mode=True)
    interpreter.run()
    marks = interpreter.get_marks()
    feedback = interpreter.get_feedback()
    write_to_file("./comments.txt", "\n\n".join(feedback))
    write_json_to_file("./marks.json", marks)
    interpreter.print_warnings()

    # write_to_file("temp/feedback.txt", feedback)


if __name__ == "__main__":
    main_func()
