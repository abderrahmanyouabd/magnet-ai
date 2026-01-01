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
