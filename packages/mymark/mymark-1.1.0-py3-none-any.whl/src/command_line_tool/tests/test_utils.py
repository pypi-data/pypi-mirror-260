import os.path

from src.command_line_tool import utils


def test_get_file_contents() -> None:
    filepath = "./src/command_line_tool/tests/dummy_files/hello_world.txt"
    assert utils.get_file_contents(os.path.abspath(filepath)) == "Hello World"


def test_write_to_file() -> None:
    filepath = "./src/command_line_tool/tests/write_test.txt"
    utils.write_to_file(os.path.abspath(filepath), "foo")
    with open(os.path.abspath(filepath), "r") as f:
        contents = f.read()
        assert contents == "foo"


def test_generate_query() -> None:
    instructions = "Write a python program that prints 'Hello World'"
    code = ""
    assert (
        utils.generate_query(code, instructions)
        == "Tell a student that wrote the following code whether they have successfully done"
        " everything in instructions and if not advise them on how they should implement them"
        " without revealing the instructions:\n\nInstructions:\nWrite a python program that"
        " prints 'Hello World'\n\nCode:\n"
    )
