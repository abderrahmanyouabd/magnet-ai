import unittest
from unittest.mock import patch
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
import os
from config import MAX_CHARS

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
        
        self.assertEqual(result, "Error: Directory ../unsafe is not within the working directory safe")

    @patch('os.path.abspath')
    @patch('os.listdir')
    def test_get_files_info_empty_dir(self, mock_listdir, mock_abspath):
        mock_abspath.side_effect = lambda x: f"/path/to/{x}"
        mock_listdir.return_value = []
        
        result = get_files_info('work')
        
        self.assertEqual(result, "")

class TestGetFileContent(unittest.TestCase):
    @patch('os.path.isfile')
    @patch('os.path.abspath')
    @patch('builtins.open', create=True)
    def test_get_file_content_small_file(self, mock_open, mock_abspath, mock_isfile):
        # Setup: Create a small file (500 chars)
        small_content = "A" * 500
        mock_abspath.side_effect = lambda x: f"/abs/{x}"
        mock_isfile.return_value = True
        mock_open.return_value.__enter__.return_value.read.return_value = small_content
        
        # Execute
        result = get_file_content('/work', 'test.txt')
        
        # Verify: Should return full content without truncation message
        self.assertEqual(result, small_content)
        self.assertNotIn("truncated", result)
        self.assertEqual(len(result), 500)

    @patch('os.path.isfile')
    @patch('os.path.abspath')
    @patch('builtins.open', create=True)
    def test_get_file_content_large_file_truncated(self, mock_open, mock_abspath, mock_isfile):
        # Setup: Create a large file (15000 chars, larger than MAX_CHARS=10000)
        large_content = "B" * (MAX_CHARS + 5000)  # Simulate that read(MAX_CHARS) returns exactly MAX_CHARS
        mock_abspath.side_effect = lambda x: f"/abs/{x}"
        mock_isfile.return_value = True
        mock_open.return_value.__enter__.return_value.read.return_value = large_content
        
        # Execute
        result = get_file_content('/work', 'large.txt')
        
        # Verify: Should contain truncation message
        self.assertIn("truncated", result)
        self.assertGreater(len(result), MAX_CHARS)  # Should be larger due to truncation message
        self.assertTrue(result.startswith("B" * 100))  # First part should be the content
    
    @patch('os.path.isfile')
    @patch('os.path.abspath')
    def test_get_file_content_file_not_found(self, mock_abspath, mock_isfile):
        mock_abspath.side_effect = lambda x: f"/abs/{x}"
        mock_isfile.return_value = False
        
        result = get_file_content('/work', 'test.txt')
        
        self.assertEqual(result, "Error: File test.txt does not exist")

if __name__ == '__main__':
    unittest.main()
