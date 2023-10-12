import argparse
import glob
import os
import shutil

from server.uploads.file_manager import FileManager


def copy_file(source: str, target: str) -> None:
    FileManager.ensure_directory_exists(target)
    shutil.copy(source, target)

def copy_all_files(include_pattern, exclude_patterns) -> None:
    files = glob.glob(include_pattern)
    for file in files:
        if not can_copy_file(file, exclude_patterns):
            continue


    pass

def can_copy_file(path, exclude_patterns) -> bool:
    for pattern in exclude_patterns:
        if pattern in path:
            return False

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move server files from this project to target destination.")

    parser.add_argument("--target", required=True, help="Target directory for moving files.")
    args = parser.parse_args()

    target_directory = args.target
    current_file = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.join(current_file, "..")

    files_to_move = [
        "wsgi.py",
        "requirements.txt"
    ]

    folder_searches = [
        {"includes": ["uploads/**/*.py"], "excludes": ["tests"]}
    ]

    for file in files_to_move:
        path = os.path.join(root_path, file)
        target = os.path.join(target_directory, file)
        copy_file(path, target)

    for folder_search in folder_searches:
        for include_pattern in folder_search["includes"]:
            copy_all_files(include_pattern, folder_search["excludes"])
        pass
