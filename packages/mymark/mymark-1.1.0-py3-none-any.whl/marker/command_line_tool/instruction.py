from __future__ import annotations

import re
from enum import Enum
from typing import Optional

import adapter.adapter_server as adapter
from command_line_tool.utils import JsonBlob


class PromptType(str, Enum):
    CONST = "const"
    BOOL = "bool"
    LIST = "list"
    ASSERT = "assert"
    FOR_EACH = "for_each"


class Instruction:
    def __init__(
        self,
        name: str,
        number: str,
        definition: JsonBlob,
        code: str,
        files: dict[str, str],
        debug_mode: bool = False,
        debug_folder_path: Optional[str] = None,
        instruction_parts: Optional[list[str]] = None,
    ) -> None:
        self.name = name
        self.number = number
        self.definition = definition
        self.code = code
        self.files = files
        self.debug_mode = debug_mode
        self.debug_folder_path = debug_folder_path
        self.current_queries: list[tuple[adapter.GPTRole, str]] = []
        self.prompts = list(range(len(self.definition["prompts"])))
        self.attribute_names = []
        self.current_prompts: list[int] = []

        if instruction_parts:
            for i, instruction_part in enumerate(instruction_parts):
                instruction_parts[i] = instruction_part.strip()
            if len(instruction_parts) - 1 != len(self.definition["inputs"]):
                raise ValueError(
                    f"Invalid number of arguments to instruction {number[:-1]}:"
                    f" expected {len(self.definition['inputs'])} but got"
                    f" {len(instruction_parts) - 1}!"
                )

            for i, var_name in enumerate(self.definition["inputs"]):
                setattr(self, var_name, instruction_parts[i + 1])
                self.attribute_names.append(var_name)

    def done(self) -> bool:
        return not self.prompts

    def get_variables_used(self, prompt: JsonBlob) -> list[str]:
        variables_used = []
        if (
            prompt["type"] == PromptType.CONST
            or prompt["type"] == PromptType.BOOL
            or prompt["type"] == PromptType.LIST
        ):
            variables_used = re.findall(r"{(\w+)}", prompt["string"]) + prompt.get("files", [])
        elif prompt["type"] == PromptType.ASSERT:
            variables_used = re.findall(r"{(\w+)}", prompt["condition"]) + re.findall(
                r"{(\w+)}", prompt["feedback"]
            )
        else:
            raise ValueError(f"Unknown prompt type: {prompt['type']}")
        return variables_used

    def check_prompt_ready(self, prompt: JsonBlob) -> bool:
        variables_used = self.get_variables_used(prompt)
        for variable in variables_used:
            if not hasattr(self, variable):
                return False
        return True

    def get_ready_prompts(self) -> list[int]:
        ready_prompts = []
        for prompt_number in self.prompts:
            if self.check_prompt_ready(self.definition["prompts"][prompt_number]):
                ready_prompts.append(prompt_number)
        for prompt_number in ready_prompts:
            self.prompts.remove(prompt_number)
        return ready_prompts

    def generate_query(self, prompt: JsonBlob) -> tuple[adapter.GPTRole, str]:
        variables_used = self.get_variables_used(prompt)
        var_dict = {var: getattr(self, var) for var in variables_used}
        query = prompt["string"].format(**var_dict)
        if prompt.get("files"):
            code_in_files = True
            for file_name in prompt["files"]:
                if not self.files.get(getattr(self, file_name)):
                    print(f"Warning: file not found {file_name}! Defaulting to all code.")
                    code = self.code
                    code_in_files = False
                    break
            if code_in_files:
                code = "\n\n\n\n".join(
                    [self.files[getattr(self, file_name)] for file_name in prompt["files"]]
                )
        else:
            code = self.code
        full_query = f"In the following code, {query}\n\nCode:\n{code}"
        return (adapter.GPTRole.USER, full_query)

    def check_assertion(self, prompt: JsonBlob) -> Optional[str]:
        variables_used = self.get_variables_used(prompt)
        var_dict = {var: getattr(self, var) for var in variables_used}
        if not eval(prompt["condition"].format(**var_dict)):
            assert isinstance(prompt["feedback"], str)
            return prompt["feedback"].format(**var_dict)
        return None

    def process_prompts(self) -> tuple[list[tuple[adapter.GPTRole, str]], list[str]]:
        ret_feedback = []
        ready_prompts = self.get_ready_prompts()
        self.current_prompts = []
        if not ready_prompts:
            print(self.prompts)
            print(self.get_ready_prompts())
            raise RuntimeError("Error: Bad instruction definition! Cannot proceed.")
        queries = []
        for prompt_number in ready_prompts:
            prompt = self.definition["prompts"][prompt_number]
            if (
                prompt["type"] == PromptType.CONST
                or prompt["type"] == PromptType.BOOL
                or prompt["type"] == PromptType.LIST
            ):
                queries.append(self.generate_query(prompt))
                self.current_prompts.append(prompt_number)
            elif prompt["type"] == PromptType.ASSERT:
                feedback = self.check_assertion(prompt)
                if feedback:
                    ret_feedback.append(f"{self.number} {feedback}")
            elif prompt["type"] == PromptType.FOR_EACH:
                raise NotImplementedError("'For each' not yet implemented")
            else:
                raise ValueError(f"Unknown prompt type: {prompt['type']}")
        if self.debug_mode:
            self.current_queries = queries
        return queries, ret_feedback

    def process_single_feedback(self, prompt: JsonBlob, feedback: str) -> None:
        match prompt["type"]:
            case PromptType.CONST:
                setattr(self, prompt["returns"], feedback)
                self.attribute_names.append(prompt["returns"])
            case PromptType.BOOL:
                setattr(self, prompt["returns"], "yes" in feedback.lower())
                self.attribute_names.append(prompt["returns"])
            case PromptType.LIST:
                setattr(self, prompt["returns"], [item.strip() for item in feedback.split(",")])
                self.attribute_names.append(prompt["returns"])
            case _:
                raise ValueError(f"Error: Unknown prompt type \"{prompt['type']}\"")

    def process_feedback(self, all_feedback: list[str]) -> None:
        for i, feedback in enumerate(all_feedback):
            if self.debug_mode:
                print(
                    f"Prompt: {self.definition['prompts'][self.current_prompts[i]]}\nQuery:"
                    f" {self.current_queries[i][1][:self.current_queries[i][1].find('Code:')]}"
                    f"\nFeedback: {feedback}\n"
                )
            self.process_single_feedback(
                self.definition["prompts"][self.current_prompts[i]], feedback
            )

    def get_sub_instructions(self) -> list[Instruction]:
        sub_instructions = []
        sub_instruction_defs = self.definition["sub_instructions"]
        for sub_instruction_def in sub_instruction_defs:
            for value in getattr(self, sub_instruction_def["list"]):
                instruction = Instruction(
                    sub_instruction_def["name"],
                    self.number,
                    sub_instruction_def,
                    self.code,
                    self.files,
                    debug_mode=self.debug_mode,
                    debug_folder_path=self.debug_folder_path,
                )
                setattr(instruction, sub_instruction_def["variable"], value)
                instruction.attribute_names.append(sub_instruction_def["variable"])
                for attribute_name in self.attribute_names:
                    setattr(instruction, attribute_name, getattr(self, attribute_name))
                    instruction.attribute_names.append(attribute_name)
                sub_instructions.append(instruction)
        return sub_instructions
