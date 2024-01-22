import os
import unittest
from ..file_stats import get_overview_stats


class TestFileStats(unittest.TestCase):
    def test_get_overview_stats(self) -> None:
        root_dir = os.path.dirname(os.path.abspath(__file__))
        test_files = os.path.join(root_dir, "test_files")

        stats, child_stats = get_overview_stats(test_files)
        assert stats['total_files'] == 3
        assert stats['total_size'] == 60
        assert stats['file_sizes'] == 30
        assert stats['files'] == 2
        assert stats['name'] == '.'

        assert child_stats[0][0] == 'c'

        assert child_stats[0][1][0]['file_sizes'] == 30
        assert child_stats[0][1][0]['files'] == 1
        assert child_stats[0][1][0]['total_files'] == 1
        assert child_stats[0][1][0]['total_size'] == 30
