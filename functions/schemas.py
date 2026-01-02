from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their size and is_dir (if it is a directory or not)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_dir": types.Schema(
                type=types.Type.STRING,
                description="The working directory",
            ),
            "dir": types.Schema(
                type=types.Type.STRING,
                description="The directory to get information about",
            ),
        },
        required=["working_dir"],
    ),
)


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a given file as a string.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "work_dir": types.Schema(
                type=types.Type.STRING,
                description="The working directory",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to get content from.",
            ),
        },
        required=["work_dir", "file_path"],
    ),
)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file in the specified directory. The file is executed in non-interactive mode by default. If you want to run it in interactive mode, set the interactive parameter to True. its takes also cli arguments to pass to the script.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "work_dir": types.Schema(
                type=types.Type.STRING,
                description="The working directory",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to run.",
            ),
            "timeout": types.Schema(
                type=types.Type.INTEGER,
                description="The maximum execution time in seconds (default: 30)",
            ),
            "interactive": types.Schema(
                type=types.Type.BOOLEAN,
                description="If True, allows user interaction (input prompts visible)",
            ),
            "cli_args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command-line arguments to pass to the script (e.g., ['--input', 'file.txt', '--verbose'])",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["work_dir", "file_path"],
    ),
)


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a string to a file in the specified directory. If the file does not exist, it will be created. If the file already exists, it will be overwritten or updated based on arguments provided. If start_line and end_line are None: Overwrites entire file with content. If start_line and end_line are provided: Replaces lines [start_line, end_line] with content. If target_content is provided: Validates that the target range matches before replacing.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "work_dir": types.Schema(
                type=types.Type.STRING,
                description="The working directory",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
            "target_content": types.Schema(
                type=types.Type.STRING,
                description="The content to replace in the file. Optional.",
            ),
            "start_line": types.Schema(
                type=types.Type.INTEGER,
                description="The starting line number (1-indexed, inclusive). Optional.",
            ),
            "end_line": types.Schema(
                type=types.Type.INTEGER,
                description="The ending line number (1-indexed, inclusive). Optional.",
            ),
        },
        required=["work_dir", "file_path", "content"],
    ),
)