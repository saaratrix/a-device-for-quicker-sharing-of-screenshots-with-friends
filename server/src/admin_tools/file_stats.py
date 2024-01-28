import os
from typing import Tuple, List, Dict, Union

Stats = Dict[str, Union[int, str]]
ChildStats = List[Tuple[str, List[Union[Stats, 'ChildStats']]]]


def get_directory_stats(directory: str, root: str) -> Tuple[Stats, ChildStats]:
    file_sizes = 0
    files = 0
    child_sizes = 0
    child_count = 0
    child_stats = []
    path = os.path.relpath(directory, root)
    name = os.path.basename(directory)

    for entry in os.scandir(directory):
        if entry.is_file():
            file_sizes += entry.stat().st_size
            files += 1
        elif entry.is_dir():
            dir_stats, dir_child_stats = get_directory_stats(entry.path, root)
            child_stats.append((dir_stats['name'], [dir_stats, dir_child_stats]))
            child_count += dir_stats['total_files']
            child_sizes += dir_stats['total_size']

    total_size = file_sizes + child_sizes
    total_files = files + child_count

    stats = {'name': name, 'path': path, 'file_sizes': file_sizes, 'files': files, 'total_size': total_size, 'total_files': total_files}
    return stats, child_stats


def get_overview_stats(directory: str) -> Tuple[Stats, ChildStats]:
    # This is more for unit tests by CI that can't read the directory.
    if not os.path.exists(directory):
        return {'name': '', 'path': '.', 'file_sizes': 0, 'files': 0, 'total_size': 0, 'total_files': 0}, []

    stats, child_stats = get_directory_stats(directory, directory)
    return stats, child_stats
