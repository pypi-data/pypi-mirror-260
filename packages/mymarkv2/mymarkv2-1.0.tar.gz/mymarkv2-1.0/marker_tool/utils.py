import glob
import json
import os
from typing import Any, Optional, Union

JsonBlob = dict[str, Any]


def get_file_contents(path: str) -> str:
    """Returns contents of given file"""
    with open(path, "r") as f:
        instructions = f.read()
    return instructions


def get_folder_contents(path: str) -> dict[str, str]:
    """Returns file name and contents of all files in folder"""
    all_files = glob.glob(f"{path}/**/*", recursive=True)
    code_files = [f for f in all_files if os.path.isfile(f)]
    top_level_folder_name = (
        path[path.rfind("\\") + 1 :] if "\\" in path else path[path.rfind("/") + 1 :]
    )
    all_code = {}
    for file_path in code_files:
        with open(file_path, "r") as f:
            file_name = top_level_folder_name + file_path[len(path) :]
            all_code[file_name] = file_name + ":\n\n" + f.read()
    return all_code


def get_folder_files(path: str) -> list[str]:
    all_files = glob.glob(f"{path}/**/*", recursive=True)
    code_files = [f for f in all_files if os.path.isfile(f)]
    files = []
    for file_path in code_files:
        with open(file_path, "r") as f:
            files.append(f.read())
    return files


def write_to_file(path: str, contents: str) -> None:
    """Writes a string to the given file"""
    with open(path, "w") as f:
        f.write(contents)


def write_json_to_file(path: str, contents: Union[dict, list]) -> None:
    """Writes a string to the given file"""
    with open(path, "w") as f:
        json.dump(contents, f)


def generate_query(code: str, instructions: str, debug_file_path: Optional[str] = None) -> str:
    """Injects code and instructions into a query and returns the query"""
    query = (
        "Tell a student that wrote the following code whether they have successfully done"
        " everything in instructions and if not advise them on how they should implement them"
        f" without revealing the instructions:\n\nInstructions:\n{instructions}\n\nCode:\n{code}"
    )
    if debug_file_path:
        write_to_file(debug_file_path, query)
    return query


def generate_queries(code: str, instructions: str, debug_file_path: Optional[str] = None) -> str:
    """Injects code and instructions into a query and returns the query"""
    query = (
        "Tell a student that wrote the following code whether they have successfully done"
        " everything in instructions and if not advise them on how they should implement them"
        f" without revealing the instructions:\n\nInstructions:\n{instructions}\n\nCode:\n{code}"
    )
    if debug_file_path:
        write_to_file(debug_file_path, query)
    return query
