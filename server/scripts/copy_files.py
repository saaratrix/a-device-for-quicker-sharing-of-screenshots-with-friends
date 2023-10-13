import argparse
import glob
import os
import shutil


# Copied from file_manager ensure_directory_exists()
def ensure_directory_exists(file_path: str) -> None:
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory, 0o777, True)


def copy_file(source: str, target: str) -> None:
    source_abs = os.path.abspath(source)
    target_abs = os.path.abspath(target)

    print(f"Copied {source} to {target}")
    ensure_directory_exists(target_abs)
    shutil.copy2(source_abs, target_abs)


def copy_all_files(include_pattern, exclude_patterns) -> None:
    files = glob.glob(include_pattern, recursive=True)
    for file in files:
        if not can_copy_file(file, exclude_patterns):
            continue

        relative_path = file.replace(root_path, "")
        target_file = os.path.join(target_directory, relative_path)
        copy_file(file, target_file)


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
    root_path = os.path.abspath(os.path.join(current_file, "..", ""))
    # Check if the last character of root_path is not a slash or backslash
    if not root_path.endswith(os.path.sep):
        root_path = os.path.join(root_path, "")

    files_to_move = [
        "wsgi.py",
        "requirements.txt"
    ]

    folder_searches = [
        {"includes": ["uploads/**/*.py"], "excludes": ["tests"]}
    ]

    for file_to_move in files_to_move:
        path = os.path.join(root_path, file_to_move)
        target = os.path.join(target_directory, file_to_move)
        copy_file(path, target)

    for folder_search in folder_searches:
        for include_pattern in folder_search["includes"]:
            # Need to include the path or the glob doesn't work.
            include_pattern = os.path.join(root_path, include_pattern)
            copy_all_files(include_pattern, folder_search["excludes"])
        pass

    print("Finished copy all files.")
