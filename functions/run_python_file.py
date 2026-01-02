import os
import subprocess
import sys


def run_python_file(work_dir, file_path, timeout=30, interactive=False, cli_args=None):
    """
    Run a Python file in its proper working directory using subprocess.
    
    Args:
        work_dir (str): Working directory where the file is located
        file_path (str): Relative path to the Python file
        timeout (int): Maximum execution time in seconds (default: 30)
        interactive (bool): If True, allows user interaction (input prompts visible)
        cli_args (list): Optional list of command-line arguments to pass to the script
    
    Returns:
        str: Output from the script or error message
    
    Examples:
        # Run without arguments
        run_python_file('.', 'script.py')
        
        # Run with arguments
        run_python_file('.', 'script.py', cli_args=['--input', 'data.txt', '--verbose'])
    """
    abs_working_dir = os.path.abspath(work_dir)
    abs_file_path = os.path.abspath(os.path.join(work_dir, file_path))
    
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: File {file_path} is not within the working directory {work_dir}"
    
    if not os.path.isfile(abs_file_path):
        return f"Error: File {file_path} does not exist"
    
    if not abs_file_path.endswith(".py"):
        return f"Error: File {file_path} is not a Python file"
    
    # Build command: [python, script.py, arg1, arg2, ...]
    command = [sys.executable, abs_file_path]
    if cli_args:
        if isinstance(cli_args, list):
            command.extend(cli_args)
        else:
            return f"Error: cli_args must be a list, got {type(cli_args)}"
    
    try:
        if interactive:
            # Interactive mode: Connect subprocess to terminal (shows prompts)
            result = subprocess.run(
                command,
                cwd=abs_working_dir,
                timeout=timeout
            )
            
            # In interactive mode, output goes directly to terminal
            if result.returncode != 0:
                return f"\nError: Script exited with code {result.returncode}"
            return f"\nSuccess: Script completed"
        else:
            # Non-interactive mode: Capture output
            result = subprocess.run(
                command,
                cwd=abs_working_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                output += result.stderr
            
            if result.returncode != 0:
                return f"Error: Script exited with code {result.returncode}\n{output}"
            
            return output if output else f"Success: File {file_path} executed successfully (no output)"
        
    except subprocess.TimeoutExpired:
        return f"Error: Script execution timed out after {timeout} seconds"
    except Exception as e:
        return f"Error: {e}"