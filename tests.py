import unittest
from unittest.mock import patch, mock_open, MagicMock
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
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

class TestWriteFile(unittest.TestCase):
    @patch('os.path.isfile')
    @patch('os.path.abspath')
    @patch('os.path.join')
    @patch('builtins.open', new_callable=mock_open)
    def test_write_file_full_overwrite(self, mock_file, mock_join, mock_abspath, mock_isfile):
        """Test full file overwrite (no line ranges)"""
        mock_join.return_value = '/work/test.py'
        mock_abspath.side_effect = lambda x: f"/abs{x}" if x.startswith('/') else f"/abs/{x}"
        
        result = write_file('/work', 'test.py', 'print("Hello")\n')
        
        # Verify file was opened in write mode
        mock_file.assert_called_once_with('/abs/work/test.py', 'w', encoding='utf-8')
        # Verify content was written
        mock_file().write.assert_called_once_with('print("Hello")\n')
        self.assertIn("Success", result)
    
    @patch('os.path.isfile')
    @patch('os.path.abspath')
    @patch('builtins.open', new_callable=mock_open)
    def test_write_file_line_splice_without_validation(self, mock_file, mock_abspath, mock_isfile):
        """Test line-based replacement without target validation"""
        mock_abspath.side_effect = lambda x: f"/abs/{x}"
        mock_isfile.return_value = True
        
        # Mock file content: 5 lines
        original_content = "line1\nline2\nline3\nline4\nline5\n"
        mock_file.return_value.readlines.return_value = original_content.splitlines(keepends=True)
        
        # Replace lines 2-3 with new content
        result = write_file('/work', 'test.py', 'new_line\n', start_line=2, end_line=3)
        
        # Verify success
        self.assertIn("Success", result)
        self.assertIn("[2, 3]", result)
        
        # Verify the spliced content
        handle = mock_file()
        written_lines = []
        for call in handle.writelines.call_args_list:
            written_lines.extend(call[0][0])
        
        expected = ['line1\n', 'new_line\n', 'line4\n', 'line5\n']
        self.assertEqual(written_lines, expected)
    
    @patch('os.path.isfile')
    @patch('os.path.abspath')
    @patch('builtins.open', new_callable=mock_open)
    def test_write_file_line_splice_with_validation_success(self, mock_file, mock_abspath, mock_isfile):
        """Test line-based replacement with target validation (matching content)"""
        mock_abspath.side_effect = lambda x: f"/abs/{x}"
        mock_isfile.return_value = True
        
        # Mock file content
        original_content = "line1\nold_code()\nline3\n"
        mock_file.return_value.readlines.return_value = original_content.splitlines(keepends=True)
        
        # Replace line 2 with validation
        result = write_file(
            '/work', 'test.py', 
            'new_code()\n',
            target_content='old_code()\n',
            start_line=2, 
            end_line=2
        )
        
        # Verify success
        self.assertIn("Success", result)
    
    @patch('os.path.isfile')
    @patch('os.path.abspath')
    @patch('builtins.open', new_callable=mock_open)
    def test_write_file_line_splice_with_validation_failure(self, mock_file, mock_abspath, mock_isfile):
        """Test line-based replacement with target validation (mismatched content)"""
        mock_abspath.side_effect = lambda x: f"/abs/{x}"
        mock_isfile.return_value = True
        
        # Mock file content
        original_content = "line1\nactual_code()\nline3\n"
        mock_file.return_value.readlines.return_value = original_content.splitlines(keepends=True)
        
        # Try to replace with wrong target content
        result = write_file(
            '/work', 'test.py', 
            'new_code()\n',
            target_content='expected_code()\n',  # This doesn't match actual content
            start_line=2, 
            end_line=2
        )
        
        # Verify error
        self.assertIn("Error: Target content mismatch", result)
    
    @patch('os.path.abspath')
    def test_write_file_path_traversal_attack(self, mock_abspath):
        """Test security: prevent path traversal attacks"""
        mock_abspath.side_effect = lambda x: "/safe" if x == "/safe" else "/unsafe"
        
        result = write_file('/safe', '../unsafe/file.txt', 'malicious')
        
        self.assertIn("Error: File ../unsafe/file.txt is not within the working directory", result)
    
    @patch('os.path.isfile')
    @patch('os.path.abspath')
    def test_write_file_file_not_found(self, mock_abspath, mock_isfile):
        """Test error when trying to splice a non-existent file"""
        mock_abspath.side_effect = lambda x: f"/abs/{x}"
        mock_isfile.return_value = False
        
        result = write_file('/work', 'missing.py', 'content', start_line=1, end_line=1)
        
        self.assertIn("Error: File missing.py does not exist", result)
    
    @patch('os.path.isfile')
    @patch('os.path.abspath')
    @patch('builtins.open', new_callable=mock_open)
    def test_write_file_invalid_line_range(self, mock_file, mock_abspath, mock_isfile):
        """Test error for invalid line ranges"""
        mock_abspath.side_effect = lambda x: f"/abs/{x}"
        mock_isfile.return_value = True
        
        # Test 1: start_line < 1
        result = write_file('/work', 'test.py', 'content', start_line=0, end_line=5)
        self.assertIn("Error: Invalid line range", result)
        
        # Test 2: end_line < start_line
        result = write_file('/work', 'test.py', 'content', start_line=5, end_line=2)
        self.assertIn("Error: Invalid line range", result)
    
    @patch('os.path.isfile')
    @patch('os.path.abspath')
    @patch('builtins.open', new_callable=mock_open)
    def test_write_file_line_range_exceeds_file(self, mock_file, mock_abspath, mock_isfile):
        """Test error when line range exceeds file length"""
        mock_abspath.side_effect = lambda x: f"/abs/{x}"
        mock_isfile.return_value = True
        
        # Mock file with only 3 lines
        original_content = "line1\nline2\nline3\n"
        mock_file.return_value.readlines.return_value = original_content.splitlines(keepends=True)
        
        # Try to replace lines beyond file length
        result = write_file('/work', 'test.py', 'content', start_line=1, end_line=10)
        
        self.assertIn("Error: end_line 10 exceeds file length 3", result)

if __name__ == '__main__':
    unittest.main()
