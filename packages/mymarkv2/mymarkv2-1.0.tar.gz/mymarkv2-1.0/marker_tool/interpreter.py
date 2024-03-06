import os
from functools import partial
from typing import Any, Callable, Optional, Union

import adapter.adapter_server as adapter
from adapter.adapter_server import GPTRole
from marker_tool.utils import JsonBlob, get_folder_contents, write_to_file


class Interpreter:
    def __init__(
        self,
        module_name: str,
        exercise_name: str,
        code_path: str,
        debug_mode: bool = False,
        debug_folder_path: str = "temp",
        indent_size: int = 4,
        mark_scheme_string: Optional[str] = None,
    ) -> None:
        self.debug_folder_path = debug_folder_path
        self.debug_mode = debug_mode
        self.indent_size = indent_size
        self.server_adapter = adapter.ServerAdapter()
        self.query_index = 1
        self.file_stack: list[list[str]] = []
        self.indent_stack: list[Callable[[], Any]] = []
        self.indent = 0
        self.marks: JsonBlob = {}
        self.successes = 0
        self.failures = 0
        self.class_name: Optional[str] = None
        self.function_name: Optional[str] = None
        self.variables: JsonBlob = {}
        self.for_loop_data: list[JsonBlob] = []
        self.warnings: list[str] = []
        self.feedback_queries: list[str] = []
        self.feedback: list[str] = []
        self.lines: list[str] = []
        self.feedback_queries_full: list[tuple[str, str]] = []
        self.debug_string = ""
        self.first_pass = False
        self.line = 0
        self.mark_scheme_string = mark_scheme_string
        self.mark_scheme = (
            self.mark_scheme_string
            if self.mark_scheme_string is not None
            else self.server_adapter.get_mark_scheme(module_name, exercise_name)
        )
        self.module_name = module_name
        self.exercise_name = exercise_name
        self.code_path = code_path

        if self.debug_folder_path and not os.path.exists(self.debug_folder_path):
            os.mkdir(self.debug_folder_path)

        if code_path[-1] == "\\" or code_path[-1] == "/":
            code_path = code_path[:-1]
        self.files = get_folder_contents(code_path)
        self.code = "\n\n\n\n".join(self.files.values())

    def get_indent(self, line: str) -> int:
        return (len(line) - len(line.lstrip())) // self.indent_size

    def generate_query(
        self,
        query: str,
        response_type: Optional[str] = None,
        assertion: bool = False,
        feedback: bool = False,
    ) -> str:
        if query[-1] != "?" and not feedback:
            query += "?"
        elif query[-1] != "." and feedback:
            query += "."
        if assertion:
            if self.class_name and self.function_name:
                prefix = (
                    f"In the following code, in the class {self.class_name}, in the function "
                    f"{self.function_name}, is it true that "
                )
            elif self.function_name:
                prefix = (
                    f"In the following code, in the function {self.function_name}, is it true that "
                )
            elif self.class_name:
                prefix = f"In the following code, in the class {self.class_name}, is it true that "
            else:
                prefix = "In the following code, is it true that "
        elif feedback:
            if self.class_name and self.function_name:
                prefix = f"in the class {self.class_name}, in the function {self.function_name}, "
            elif self.function_name:
                prefix = f"in the function {self.function_name}, "
            elif self.class_name:
                prefix = f"in the class {self.class_name}, "
            else:
                prefix = ""
            prefix = (
                "In the following code, give feedback to a student who has not met the "
                f"following criteria without writing any code: {prefix}"
            )
        else:
            if self.class_name and self.function_name:
                prefix = (
                    f"In the following code, in the class {self.class_name}, in the "
                    f"function {self.function_name}, "
                )
            elif self.function_name:
                prefix = f"In the following code, in the function {self.function_name}, "
            elif self.class_name:
                prefix = f"In the following code, in the class {self.class_name}, "
            else:
                prefix = "In the following code, "
        query = prefix + query
        match response_type:
            case "const":
                query = (
                    f"{query} Don't include any explanations in your response. Don't include "
                    "the question in your response."
                )
            case "bool":
                query = (
                    f"{query} Answer 'Yes' or 'No'. Don't include any explanations in your "
                    "response. Don't include the question in your response."
                )
            case "list":
                query = (
                    f"{query} Give your answer as a csv. Don't include any explanations in "
                    "your response. Don't include the question in your response."
                )
            case "class":
                query = (
                    f"{query} Return only the class name. Don't include any explanations in "
                    "your response. Don't include the question in your response."
                )
            case "function":
                query = (
                    f"{query} Return only the function name. Don't include any explanations "
                    "in your response. Don't include the question in your response."
                )
            case "file":
                query = (
                    f"{query} Return only the file path. Don't include any explanations in "
                    "your response. Don't include the question in your response."
                )
            case "feedback":
                query = (
                    f"{query} Don't include the question in your response. Respond with at "
                    "most a couple of sentences."
                )
            case None:
                pass
            case _:
                raise ValueError(f"Invalid response type: {response_type}")

        code = ""
        add_all_code = False
        if self.file_stack:
            for file_name in self.file_stack[-1]:
                if file_code := self.files.get(file_name):
                    code += file_code + "\n\n\n\n"
                else:
                    if not self.first_pass:
                        warning = f"Warning: file not found {file_name}! Defaulting to all code."
                        print(warning)
                        self.warnings.append(warning)
                    add_all_code = True
                    break
        else:
            add_all_code = True

        if add_all_code:
            code = self.code

        query += f"\n\nCode:\n\n{code}"
        return query

    def get_gpt_response(self, query: str) -> str:
        if self.first_pass:
            return ""
        self.debug_string += query[: query.find("Code:")].strip() + "\n\n"
        if self.debug_mode:
            print(f"Sending query: {query[:query.find('Code:')].strip()}")
        response = self.server_adapter.get_response(
            adapter.GPTRequest(
                [{"content": query, "role": GPTRole.USER}],
                temperature=0,
                model=adapter.GPTModel.GPT3_5TURBO_UNLIMITED,
            )
        )
        self.debug_string += response + "\n\n"
        if self.debug_mode:
            print(f"Response: {response}\n")
            write_to_file(f"{self.debug_folder_path}/query_{self.query_index}.txt", query)
            write_to_file(f"{self.debug_folder_path}/reponse_{self.query_index}.txt", response)
            self.query_index += 1
        return str(response)

    def send_query(
        self,
        query: str,
        response_type: Optional[str] = None,
        assertion: bool = False,
        feedback: bool = False,
    ) -> str:
        query = self.generate_query(
            query, response_type=response_type, assertion=assertion, feedback=feedback
        )
        return self.get_gpt_response(query)

    def get_class_name(self, line: str) -> tuple[str, list[str]]:
        if '"' not in line:
            class_name = (
                line[line.find(" ") : line.find(":")]
                .strip()
                .replace("'", "")
                .format(**self.variables)
            )
        else:
            requirement = line[line.find('"') + 1 : line.rfind('"')]
            query = f"what class {requirement}"
            class_name = self.send_query(query, response_type="class")

        file_name = self.send_query(
            f"what is the file path of the file where the class '{class_name}' is defined?",
            response_type="file",
        )
        return class_name, [file_name]

    def get_function_name(self, line: str) -> tuple[str, list[str]]:
        if '"' not in line:
            function_name = (
                line[line.find(" ") : line.find(":")]
                .strip()
                .replace("'", "")
                .format(**self.variables)
            )
        else:
            requirement = line[line.find('"') + 1 : line.rfind('"')]
            query = f"what function {requirement}"
            function_name = self.send_query(query, response_type="function")

        if not self.file_stack:
            file_names = [
                self.send_query(
                    f"what is the file path of the file where the function '{function_name}' is "
                    "defined?",
                    response_type="file",
                )
            ]
        else:
            file_names = self.file_stack[-1]

        return function_name, file_names

    def get_statements(self, line: str) -> list[str]:
        statements = []
        in_statement = False
        in_variable = False
        statement = ""
        for char in line:
            if char == '"':
                if in_statement:
                    statements.append(statement)
                in_statement = not in_statement
                statement = ""
            elif in_statement:
                statement += char
            elif char == "{":
                in_variable = True
            elif char == "}":
                in_variable = False
                statements.append(("{" + statement + "}"))
                statement = ""
            elif in_variable:
                statement += char
        return statements

    def save_mark(self, criterion: str) -> None:
        self.marks[criterion]["successes"] += self.successes
        self.marks[criterion]["failures"] += self.failures
        self.marks[criterion]["feedback"][-1] += self.feedback_queries
        self.feedback_queries = []

    def calculate_mark(self, criterion: str) -> None:
        percentage = (
            self.marks[criterion]["successes"]
            / (self.marks[criterion]["successes"] + self.marks[criterion]["failures"])
            if self.marks[criterion]["successes"] + self.marks[criterion]["failures"]
            else 1.0
        )
        result = percentage * self.marks[criterion]["max_marks"]
        self.marks[criterion]["student_marks"] = max(self.marks[criterion]["student_marks"], result)
        self.marks[criterion]["successes"] = 0
        self.marks[criterion]["failures"] = 0

    def interpret_indent(self, indent: int) -> bool:
        if indent < self.indent:
            for _ in range(self.indent - indent):
                rerun = self.indent_stack[-1]()
                if rerun:
                    return True
                self.indent_stack.pop()
        self.indent = indent
        return False

    def interpret_line(self, line: str) -> None:
        if line == "end":
            return
        match line.split(" ")[0]:
            case "class":
                self.interpret_class(line)
            case "function":
                self.interpret_function(line)
            case "mark":
                self.interpret_mark(line)
            case "const":
                self.interpret_const(line)
            case "bool":
                self.interpret_bool(line)
            case "list":
                self.interpret_list(line)
            case "for":
                self.interpret_for(line)
            case "alternative":
                self.interpret_alternative(line)
            case "pass":
                pass
            case _:
                self.interpret_assertion(line)

    def interpret_assertion(self, line: str) -> None:
        initial_line = line
        in_quotes = False
        last_part = ""
        parts = []
        nots = []
        is_not = False
        i = 0
        while i < len(initial_line):
            last_part += initial_line[i]
            if initial_line[i] == '"':
                in_quotes = not in_quotes
            elif not in_quotes and initial_line[i : i + 2] == "or":
                parts.append(last_part[:-1])
                nots.append(is_not)
                last_part = ""
                break
            elif not in_quotes and initial_line[i : i + 3] == "and":
                parts.append(last_part[:-1])
                last_part = ""
                nots.append(is_not)
                is_not = False
                i += 3
            elif not in_quotes and initial_line[i : i + 3] == "not":
                is_not = not is_not
                last_part = ""
                i += 3
            i += 1
        if last_part:
            parts.append(last_part)
            nots.append(is_not)
        current_part = 0
        statements = self.get_statements(line)
        for statement in statements:
            formatted_statement = statement.format(**self.variables)
            if formatted_statement in ("True", "False"):
                response = formatted_statement == "True"
                line = line.replace(statement, str(response))
            else:
                response = (
                    "yes"
                    in self.send_query(
                        formatted_statement, response_type="bool", assertion=True
                    ).lower()
                )
                line = line.replace(f'"{statement}"', str(response))
            if current_part < len(parts) and response != nots[current_part]:
                parts.pop(current_part)
                nots.pop(current_part)
                current_part -= 1
            current_part += 1
        success = eval(line)
        if success:
            self.successes += 1
        else:
            self.failures += 1
            for i, feedback_query in enumerate(parts):
                if nots[i]:
                    feedback_query = f"it should not be true that {feedback_query}"
                else:
                    feedback_query = f"it should be true that {feedback_query}"
                self.feedback_queries.append(
                    self.generate_query(
                        feedback_query.replace('"', "").format(**self.variables),
                        response_type="feedback",
                        feedback=True,
                    )
                )

    def interpret_class(self, line: str) -> None:
        class_name, file_names = self.get_class_name(line)
        self.class_name = f"'{class_name}'"
        self.variables["class"] = f"'{class_name}'"
        self.file_stack.append(file_names)

        def deindent() -> bool:
            self.file_stack.pop()
            self.class_name = None
            self.variables.pop("class", None)
            return False

        self.indent_stack.append(deindent)

    def interpret_function(self, line: str) -> None:
        function_name, file_names = self.get_function_name(line)
        self.function_name = f"'{function_name}'"
        self.variables["function"] = f"'{function_name}'"
        self.file_stack.append(file_names)

        def deindent() -> bool:
            self.file_stack.pop()
            self.function_name = None
            self.variables.pop("function", None)
            return False

        self.indent_stack.append(deindent)

    def interpret_mark(self, line: str) -> None:
        parts = list(filter(None, line.split(" ")))
        criterion_name = parts[1].strip()
        part_name = line[line.find("'") + 1 : line.rfind("'")]
        self.successes = 0
        self.failures = 0
        if criterion_name not in self.marks:
            num_marks = parts[2].replace(":", "").strip()
            self.marks[criterion_name] = {
                "max_marks": int(num_marks),
                "student_marks": 0,
                "successes": 0,
                "failures": 0,
                "feedback": [[]],
                "part_name": part_name,
            }
        self.indent_stack.append(partial(self.save_mark, criterion_name))

    def interpret_const(self, line: str) -> None:
        first_space = line.find(" ")
        equals = line.find("=")
        const_name = line[first_space + 1 : equals].strip()
        query = (line[equals + 1 :].strip()).replace('"', "")
        response = self.send_query(query.format(**self.variables), response_type="const")
        self.variables[const_name] = response

    def interpret_bool(self, line: str) -> None:
        first_space = line.find(" ")
        equals = line.find("=")
        const_name = line[first_space + 1 : equals].strip()
        query = (line[equals + 1 :].strip()).replace('"', "")
        response = self.send_query(query.format(**self.variables), response_type="bool")
        self.variables[const_name] = "yes" in response.lower()

    def interpret_list(self, line: str) -> None:
        first_space = line.find(" ")
        equals = line.find("=")
        const_name = line[first_space + 1 : equals].strip()
        query = (line[equals + 1 :].strip()).replace('"', "")
        response = self.send_query(query.format(**self.variables), response_type="list")
        self.variables[const_name] = [item.strip() for item in response.split(",")]

    def interpret_for(self, line: str) -> None:
        first_space = line.find(" ")
        in_start = line.find(" in ")
        colon = line.find(":")
        variable = line[first_space + 1 : in_start].strip()
        list_name = line[in_start + 4 : colon].strip()
        if len(self.variables[list_name]) == 0:
            self.indent_stack.append(lambda: None)
            return
        self.for_loop_data.append(
            {"lines": [], "index": 0, "variable": variable, "list": self.variables[list_name]}
        )
        self.variables[variable] = self.variables[list_name][0]

        def deindent() -> bool:
            data = self.for_loop_data[-1]
            data["index"] += 1
            if data["index"] >= len(data["list"]):
                self.variables.pop(data["variable"], None)
                self.for_loop_data.pop()
            else:
                self.lines = data["lines"] + self.lines
                data["lines"] = []
                self.variables[data["variable"]] = data["list"][data["index"]]
                return True
            return False

        self.indent_stack.append(deindent)

    def interpret_alternative(self, line: str) -> None:
        parts = list(filter(None, line.split(" ")))
        criterion = parts[1]
        self.calculate_mark(criterion)
        self.marks[criterion]["feedback"].append([])

    def run(self) -> None:
        self.lines = self.mark_scheme.split("\n") + ["end"]
        while self.lines:
            self.line += 1
            line = self.lines.pop(0)
            for data in self.for_loop_data:
                data["lines"].append(line)
            indent = self.get_indent(line)
            line = line.strip()
            if not line or line[0] == "#":
                continue
            if self.interpret_indent(indent):
                continue
            self.interpret_line(line)

    def get_marks(self) -> list[JsonBlob]:
        total = 0
        total_correct = 0
        self.feedback_queries_full = []
        for criterion, data in self.marks.items():
            self.calculate_mark(criterion)
            total += data["max_marks"]
            total_correct += int(data["student_marks"])
            if data["max_marks"] != int(data["student_marks"]):
                for feedback_query in data["feedback"][0]:
                    self.feedback_queries_full.append((data["part_name"], feedback_query))
            data.pop("feedback")
            data.pop("successes")
            data.pop("failures")
        if self.debug_mode:
            print(self.marks | {"total": f"{total_correct}/{total}"})
        mark_dict = {}
        for data in self.marks.values():
            part_name = data["part_name"]
            if part_name not in mark_dict:
                mark_dict[part_name] = {"name": part_name, "possible": 0, "score": 0}
            mark_dict[part_name]["possible"] += data["max_marks"]
            mark_dict[part_name]["score"] += int(data["student_marks"])

        return list(mark_dict.values())

    def get_feedback(self) -> list[JsonBlob]:
        feedback_dict: JsonBlob = {}

        for part_name, query in self.feedback_queries_full:
            feedback_response = self.get_gpt_response(query)

            if part_name not in feedback_dict:
                feedback_dict[part_name] = {"name": part_name, "feedback": []}

            feedback_dict[part_name]["feedback"].append(feedback_response)

        if self.debug_mode:
            print(feedback_dict)

        return list(feedback_dict.values())

    def print_warnings(self) -> None:
        for warning in self.warnings:
            print(warning)

    def get_debug_string(self) -> str:
        return self.debug_string

    def do_first_pass(self) -> Union[int, "Interpreter"]:
        self.first_pass = True
        try:
            self.run()
        except Exception as _:
            return self.line

        return Interpreter(
            self.module_name,
            self.exercise_name,
            self.code_path,
            self.debug_mode,
            self.debug_folder_path,
            self.indent_size,
            self.mark_scheme_string,
        )
