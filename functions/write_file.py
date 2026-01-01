import os


def write_file(work_dir, file_path, content, target_content=None, start_line=None, end_line=None):
    """
    Write or modify a file using line-based splicing.
    It supports both full file overwrites and targeted line-range replacements.
    
    Args:
        work_dir (str): Working directory (for security validation)
        file_path (str): Relative path to the file
        content (str): New content to write
        target_content (str, optional): Expected content at the target range (for validation)
        start_line (int, optional): Starting line number (1-indexed, inclusive)
        end_line (int, optional): Ending line number (1-indexed, inclusive)
    
    Returns:
        str: Success message or error message
    
    Behavior:
        - If start_line and end_line are None: Overwrites entire file with content
        - If start_line and end_line are provided: Replaces lines [start_line, end_line] with content
        - If target_content is provided: Validates that the target range matches before replacing
    
    Examples:
        # Overwrite entire file
        write_file('/project', 'test.py', 'print("hello")')
        
        # Replace lines 5-10 with new content
        write_file('/project', 'test.py', 'new_code()', start_line=5, end_line=10)
        
        # Replace with validation
        write_file('/project', 'test.py', 'new_code()', 
                   target_content='old_code()', start_line=5, end_line=10)
    """
    # Security: Validate file is within working directory
    abs_working_dir = os.path.abspath(work_dir)
    abs_file_path = os.path.abspath(os.path.join(work_dir, file_path))
    
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: File {file_path} is not within the working directory {work_dir}"
    
    try:
        # Case 1: Full file overwrite (no line ranges specified)
        if start_line is None or end_line is None:
            with open(abs_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Success: File {file_path} written successfully"
        
        # Case 2: Line-based splice (targeted replacement)
        # Validate line numbers
        if start_line < 1 or end_line < start_line:
            return f"Error: Invalid line range [{start_line}, {end_line}]"
        
        # Read existing file content
        if not os.path.isfile(abs_file_path):
            return f"Error: File {file_path} does not exist"
        
        with open(abs_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Validate line range is within file bounds
        if end_line > len(lines):
            return f"Error: end_line {end_line} exceeds file length {len(lines)}"
        
        # Extract target section for validation (if target_content provided)
        if target_content is not None:
            target_section = ''.join(lines[start_line - 1:end_line])
            
            # Normalize whitespace for comparison (strip trailing whitespace on each line)
            target_normalized = '\n'.join(line.rstrip() for line in target_section.splitlines())
            expected_normalized = '\n'.join(line.rstrip() for line in target_content.splitlines())
            
            if target_normalized != expected_normalized:
                return (f"Error: Target content mismatch at lines [{start_line}, {end_line}]. "
                       f"File may have been modified. Expected:\n{expected_normalized}\n\nFound:\n{target_normalized}")
        
        # Ensure content ends with newline (unless it's meant to be empty)
        if content and not content.endswith('\n'):
            content += '\n'
        
        # Splice: before + new content + after
        new_lines = (
            lines[:start_line - 1] +           # Lines before the target range
            ([content] if content else []) +    # New content (as a single element)
            lines[end_line:]                    # Lines after the target range
        )
        
        # Write back atomically
        with open(abs_file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        return f"Success: Replaced lines [{start_line}, {end_line}] in {file_path}"
        
    except Exception as e:
        return f"Error: {e}"