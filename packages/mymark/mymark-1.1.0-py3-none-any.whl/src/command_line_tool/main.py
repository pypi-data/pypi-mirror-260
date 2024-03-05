import sys

from src.command_line_tool.dsl import DSL
from src.command_line_tool.utils import (
    write_to_file,
)


def main_func() -> None:
    """Extracts the specification and code files, calls the LLM on it and
    outputs the response"""
    if len(sys.argv) == 1:  # For debugger
        sys.argv.append(".\\user_files\\SED_example\\instructions.txt")
        sys.argv.append(".\\user_files\\SED_example\\code\\")
    if len(sys.argv) != 3:
        raise ValueError(
            f"Insufficient arguments! Expected 2 arguments but got {len(sys.argv) - 1}"
        )
    dsl = DSL("instruction_defs", sys.argv[1], sys.argv[2], "temp", debug_mode=True)
    # dsl.print_defs()
    feedback = dsl.run()
    write_to_file("temp/feedback.txt", feedback)


if __name__ == "__main__":
    main_func()
