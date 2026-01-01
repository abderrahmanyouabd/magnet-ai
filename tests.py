import unittest
from unittest.mock import patch
from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
    @patch('os.path.abspath')
    @patch('os.path.join')
    @patch('os.path.isdir')
    @patch('os.path.getsize')
    @patch('os.listdir')
    def test_get_files_info_success(self, mock_listdir, mock_getsize, mock_isdir, mock_join, mock_abspath):
        mock_abspath.side_effect = lambda x: f"/path/to/{x}"
        mock_join.side_effect = lambda a, b: f"{a}/{b}"
        mock_listdir.return_value = ['file.txt', 'folder']
        mock_isdir.side_effect = lambda path: 'folder' in path
        mock_getsize.return_value = 123
        
        result = get_files_info('work', 'dir')
        
        expected = "- file.txt: 123 bytes, is_dir: False\n- folder: 123 bytes, is_dir: True\n"
        self.assertEqual(result, expected)

    @patch('os.path.abspath')
    def test_get_files_info_traversal_attack(self, mock_abspath):
        mock_abspath.side_effect = lambda x: "/safe" if x == "safe" else "/unsafe"
        
        result = get_files_info('safe', '../unsafe')
        
        self.assertEqual(result, "Directory ../unsafe is not within the working directory safe")

    @patch('os.path.abspath')
    @patch('os.listdir')
    def test_get_files_info_empty_dir(self, mock_listdir, mock_abspath):
        mock_abspath.side_effect = lambda x: f"/path/to/{x}"
        mock_listdir.return_value = []
        
        result = get_files_info('work')
        
        self.assertEqual(result, "")

if __name__ == '__main__':
    unittest.main()
