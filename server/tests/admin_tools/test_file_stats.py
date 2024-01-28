import os
import unittest
from server.src.admin_tools.file_stats import get_overview_stats


class TestFileStats(unittest.TestCase):
    def test_get_overview_stats(self) -> None:
        root_dir = os.path.dirname(os.path.abspath(__file__))
        test_files = os.path.join(root_dir, "test_files")

        # This is confusing with a, b, c, d, e  as increment of file/folders.
        # A bad, bad idea!
        stats, child_stats = get_overview_stats(test_files)
        assert stats['total_files'] == 4
        assert stats['total_size'] == 60
        assert stats['file_sizes'] == 30
        assert stats['files'] == 2
        assert stats['name'] == 'test_files'
        assert stats['path'] == '.'

        assert child_stats[0][0] == 'c'

        assert child_stats[0][1][0]['file_sizes'] == 30
        assert child_stats[0][1][0]['files'] == 1
        assert child_stats[0][1][0]['total_files'] == 2
        assert child_stats[0][1][0]['total_size'] == 30
        assert child_stats[0][1][0]['path'] == 'c'
        assert child_stats[0][1][0]['name'] == 'c'
        # The array grows funnily per new entry, stellar design. But it does work.
        assert child_stats[0][1][1][0][1][0]['file_sizes'] == 0
        assert child_stats[0][1][1][0][1][0]['files'] == 1
        assert child_stats[0][1][1][0][1][0]['total_files'] == 1
        assert child_stats[0][1][1][0][1][0]['total_size'] == 0
        assert child_stats[0][1][1][0][1][0]['path'] == f'c{os.path.sep}e'
        assert child_stats[0][1][1][0][1][0]['name'] == 'e'
