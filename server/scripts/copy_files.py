import argparse
import glob
import os
import shutil
from typing import List, Tuple


# Copied from file_manager ensure_directory_exists()
def ensure_directory_exists(file_path: str) -> None:
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory, 0o777, True)


def copy_file(source: str, target: str, only_print_errors: bool) -> None:
    source_abs = os.path.abspath(source)
    target_abs = os.path.abspath(target)

    if not os.path.exists(source):
        print(f"\033[91mCould not copy {source} as it does not exist.[0m")
        return False

    if not only_print_errors:
        print(f"Copied {source} to {target}")

    try:
        ensure_directory_exists(target_abs)
        shutil.copy2(source_abs, target_abs)
        return True
    except Exception as e:
        print(f"\033[91mFailed to copy file {source} because {e}\033[0;0m")
        return False



def copy_all_files(include_pattern: str, exclude_patterns: List[str], only_print_errors: bool) -> Tuple[int, int]:
    files = glob.glob(include_pattern, recursive=True)
    successes = 0
    fails = 0

    for file in files:
        if not can_copy_file(file, exclude_patterns):
            continue

        relative_path = file.replace(root_path, "")
        target_file = os.path.join(target_directory, relative_path)
        if copy_file(file, target_file, only_print_errors):
            successes += 1
        else:
            fails += 1

    return successes, fails


def can_copy_file(path, exclude_patterns) -> bool:
    for pattern in exclude_patterns:
        if pattern in path:
            return False

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move server files from this project to target destination.")
    parser.add_argument("--target", required=True, help="Target directory for moving files.")
    # Add the "--venv" argument (not required with a default value)
    parser.add_argument("--venv", default="env", help="Python's venv folder path")
    args = parser.parse_args()

    venv = args.venv
    target_directory = args.target
    current_file = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.abspath(os.path.join(current_file, "..", ""))
    # Check if the last character of root_path is not a slash or backslash
    if not root_path.endswith(os.path.sep):
        root_path = os.path.join(root_path, "")

    files_to_move = [
        "wsgi.py",
        "requirements.txt"
    ]

    folder_searches = [
        {"includes": ["uploads/**/*.py"], "excludes": ["tests"], "only_print_errors": False},
        #{"includes": [f"{venv}/**/*"], "excludes": [], "only_print_errors": True}
    ]

    successes = 0
    fails = 0

    for file_to_move in files_to_move:
        path = os.path.join(root_path, file_to_move)
        target = os.path.join(target_directory, file_to_move)
        if copy_file(path, target, False):
            successes += 1
        else:
            fails += 1

    for folder_search in folder_searches:
        for include_pattern in folder_search["includes"]:
            # Need to include the path or the glob doesn't work.
            include_pattern = os.path.join(root_path, include_pattern)
            result = copy_all_files(include_pattern, folder_search["excludes"], folder_search["only_print_errors"])
            successes += result[0]
            fails += result[1]

    print("Finished copy all files.")
    print(f"Succesfully copied {successes} and failed to copy {fails}")
