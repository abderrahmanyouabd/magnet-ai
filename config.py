import os
from pathlib import Path
import platform


# HELPERS ( TODO: move to a separate file laterr)

def get_workspace_context():
    """
    Scans the current environment to build the context string.
    """
    current_uri = os.getcwd()
    corpus_name = Path(current_uri).as_posix()
    context_block = (
        f"The user has 1 active workspace, each defined by a URI and a CorpusName.\n"
        f"The mapping is shown as follows in the format [URI] -> [CorpusName]:\n"
        f"{current_uri} -> {corpus_name}\n"
    )
    return context_block


# PROMPTS & CONSTANTS


MAX_CHARS = 10000

SYSTEM_PROMPT = f"""
<identity>
You are a helpful AI coding agent.
</identity>

<instructions>
When a user asks a question or makes a request, make a function call plan. You can perform the following actions:

- List files and directories in the working directory.
</instructions>

<user_information>
The USERS's OS version is {platform.system()}
{get_workspace_context()}
You are not allowed to access files not in active workspaces.
You can only make one function call at a time.
All paths you provide should be relative to the working directory.
</user_information>
"""