import json
import re
from typing import Optional

import src.adapter.adapter_gpt as adapter
from src.command_line_tool.instruction import Instruction, PromptType
from src.command_line_tool.utils import (
    JsonBlob,
    get_file_contents,
    get_folder_contents,
    get_folder_files,
    write_to_file,
)


class DSL:
    def __init__(
        self,
        instructions_defs_path: str,
        instructions_path: str,
        code_path: str,
        debug_folder_path: Optional[str] = None,
        debug_mode: bool = False,
    ) -> None:
        instruction_defs_files = get_folder_files(instructions_defs_path)
        self.instruction_defs: JsonBlob = {}
        for file_contents in instruction_defs_files:
            self.instruction_defs |= self.parse_dsl(file_contents)

        self.debug_folder_path = debug_folder_path
        self.debug_mode = debug_mode
        self.gpt_adapter = adapter.GPTAdapter()
        self.query_index = 1

        if code_path[-1] == "\\":
            code_path = code_path[:-1]
        self.files = get_folder_contents(code_path)
        self.code = "\n\n\n\n".join(self.files.values())

        self.parse_instructions(get_file_contents(instructions_path))

    def print_defs(self) -> None:
        print(json.dumps(self.instruction_defs, indent=4))

    def get_indent(self, line: str) -> int:
        num = 0
        for char in line:
            if char.isspace():
                num += 1
            else:
                return num
        return num

    def parse_dsl(
        self,
        file_contents: str,
        outer_name: Optional[str] = None,
        instruction_def: Optional[JsonBlob] = None,
    ) -> JsonBlob:
        if instruction_def is None:
            instruction_def = {"name": None, "inputs": [], "prompts": [], "sub_instructions": []}
        lines = file_contents.split("\n")
        num_sub_instructions = 0
        line_index = 0
        while line_index < len(lines):
            line = lines[line_index].strip()
            if not line:
                pass
            elif re.match(r"^define.*\(.*\):.*$", line):
                name_start = line.find(" ") + 1
                name_end = line.find("(")
                outer_name = line[name_start:name_end]
                inputs_end = line.find(")")
                inputs = line[name_end + 1 : inputs_end].split(",")
                instruction_def["name"] = inputs[0].strip().replace('"', "")
                for instruction_input in inputs[1:]:
                    instruction_def["inputs"].append(instruction_input.strip())
            elif (
                re.match(r"^const.*=.*$", line)
                or re.match(r"^bool.*=.*$", line)
                or re.match(r"^list.*=.*$", line)
            ):
                if re.match(r"^const.*=.*$", line):
                    prompt_type = PromptType.CONST
                    suffix = (
                        "Don't include any explanations in your response.  Don't include the"
                        " question in your response."
                    )
                elif re.match(r"^bool.*=.*$", line):
                    prompt_type = PromptType.BOOL
                    suffix = "Answer 'Yes' or 'No'."
                elif re.match(r"^list.*=.*$", line):
                    prompt_type = PromptType.LIST
                    suffix = "Give your answer as a csv."
                first_space = line.find(" ")
                equals = line.find("=")
                const_name = line[first_space + 1 : equals].strip()
                last_quote = line.rfind('"')
                last_in = line.rfind(" in ")
                files = None
                if last_in and last_quote < last_in:
                    prompt_end = last_in
                    files_start = line.rfind("[")
                    files_end = line.rfind("]")
                    files = line[files_start + 1 : files_end].split(",")
                    for i, file in enumerate(files):
                        files[i] = file.strip()
                else:
                    prompt_end = -1
                prompt = (line[equals + 1 : prompt_end].strip() + " " + suffix).replace('"', "")
                instruction_def["prompts"].append(
                    {"type": prompt_type, "returns": const_name, "string": prompt}
                    | ({"files": files} if files else {})
                )
            elif re.match(r"^assert.* feedback .*$", line):
                first_space = line.find(" ")
                feedback_pos = line.find(" feedback ")
                condition = line[first_space + 1 : feedback_pos].strip()
                feedback = line[feedback_pos + 10 :].strip().replace('"', "")
                instruction_def["prompts"].append(
                    {"type": PromptType.ASSERT, "condition": condition, "feedback": feedback}
                )
            elif re.match(r"^for.* in .*$", line):
                first_space = line.find(" ")
                in_start = line.find(" in ")
                colon = line.find(":")
                variable = line[first_space + 1 : in_start]
                list_name = line[in_start + 4 : colon]
                num_sub_instructions += 1
                indent = self.get_indent(lines[line_index])
                sub_lines = []
                line_index += 1
                while line_index < len(lines):
                    if self.get_indent(lines[line_index]) <= indent:
                        line_index -= 1
                        break
                    sub_lines.append(lines[line_index])
                    line_index += 1
                sub_instruction = self.parse_dsl(
                    "\n".join(sub_lines),
                    outer_name="name",
                    instruction_def={
                        "name": instruction_def["name"],
                        "inputs": [],
                        "prompts": [],
                        "sub_instructions": [],
                    },
                )
                instruction_def["sub_instructions"].append(
                    sub_instruction["name"] | {"list": list_name, "variable": variable}
                )
            else:
                raise ValueError(f"Invalid syntax in line:\n{line}")
            line_index += 1
        assert isinstance(outer_name, str)
        return {outer_name: instruction_def}

    def parse_instructions(self, instructions: str) -> None:
        self.instructions = []
        for instruction in instructions.split("\n"):
            space_index = instruction.find(" ")
            instruction_parts = instruction[space_index + 1 :].split(",")
            instruction_number = instruction[:space_index]
            instruction_name = self.get_instruction_name(instruction_parts[0])
            this_instruction = Instruction(
                instruction_name,
                instruction_number,
                self.instruction_defs[instruction_name],
                self.code,
                self.files,
                debug_mode=self.debug_mode,
                debug_folder_path=self.debug_folder_path,
                instruction_parts=instruction_parts,
            )
            self.instructions.append(this_instruction)

    def get_instruction_name(self, name: str) -> str:
        for instruction_name in self.instruction_defs:
            if (
                self.instruction_defs[instruction_name]["name"].lower().strip()
                == name.lower().strip()
            ):
                return instruction_name
        raise ValueError(f'Invalid instruction: "{name}"')

    def run_instruction(self, instruction: Instruction) -> list[str]:
        all_feedback = []
        while not instruction.done():
            queries, feedback = instruction.process_prompts()
            for query in queries:
                if self.debug_mode:
                    write_to_file(
                        f"{self.debug_folder_path}/query_{self.query_index}.txt", query[1]
                    )
                    self.query_index += 1
            all_feedback += feedback
            if not queries:
                continue
            gpt_feedback = self.gpt_adapter.get_responses(
                [adapter.GPTRequest(q, role=role) for (role, q) in queries]
            )
            instruction.process_feedback(gpt_feedback)
        if sub_instructions := instruction.get_sub_instructions():
            for sub_instruction in sub_instructions:
                all_feedback += self.run_instruction(sub_instruction)
        return all_feedback

    def run(self) -> str:
        feedback = []
        for instruction in self.instructions:
            if instruction_feedback := self.run_instruction(instruction):
                feedback += instruction_feedback
            else:
                feedback.append(
                    f"{instruction.number} {instruction.definition['name']} is correctly"
                    " implemented."
                )
        if self.debug_mode:
            print("\n".join(feedback))
        return "\n".join(feedback)
