import unittest

from ..file_utility import FileUtility


class MyTestCase(unittest.TestCase):

    def test_get_file_extension(self):
        self.assertEqual(FileUtility.get_file_extension("m333o3ou666666u.txt"), ".txt")
        self.assertEqual(FileUtility.get_file_extension("test"), "")


if __name__ == '__main__':
    unittest.main()
