import os


def get_files_info(working_dir, dir=None):
    abs_working_dir = os.path.abspath(working_dir)
    abs_dir = None
    if dir is None:
        dir = working_dir
        abs_dir = os.path.abspath(dir)
    else:
        abs_dir = os.path.abspath(os.path.join(working_dir, dir))
    if not abs_dir.startswith(abs_working_dir):
        return f"Directory {dir} is not within the working directory {working_dir}"
    
    contents = os.listdir(abs_dir)
    final_response = ""
    for content in contents:
        is_dir = os.path.isdir(os.path.join(abs_dir, content))
        size = os.path.getsize(os.path.join(abs_dir, content))
        final_response += f"- {content}: {size} bytes, is_dir: {is_dir}\n"
    return final_response
