import os
from config import MAX_CHARS

def get_file_content(work_dir, file_path):
    abs_working_dir = os.path.abspath(work_dir)
    abs_file_path = os.path.abspath(os.path.join(work_dir, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: File {file_path} is not within the working directory {working_dir}"
    if not os.path.isfile(abs_file_path):
        return f"Error: File {file_path} does not exist"
    string_content = ""
    try:
        with open(abs_file_path, "r") as f:
            string_content = f.read(MAX_CHARS)
            if len(string_content) >= MAX_CHARS:
                string_content += f"\n[...File {abs_file_path} truncated at {MAX_CHARS} characters]"
    except Exception as e:
        return f"Error: {e}" 
    return string_content