# 🧲 Magnet AI

> **A learning project for building AI coding agents with function calling**

Magnet AI is an educational project that demonstrates how to build AI coding agents using Google's Gemini API with function calling capabilities. This project implements the same agentic patterns used by professional AI IDEs like Cursor, Windsurf, and GitHub Copilot.

## 🎯 Purpose

This project was created as a **learning resource** to understand:
- How AI coding assistants work under the hood
- Function calling and tool use patterns
- Multi-turn agentic loops
- Building autonomous AI agents that can interact with codebases

## ✨ Features

The AI agent can perform the following operations:

- **📂 List Files**: Browse directories and get file information
- **📖 Read Files**: Read file contents with truncation for large files
- **✍️ Write Files**: Create new files or update existing ones (full overwrite or line-based edits)
- **▶️ Run Python Scripts**: Execute Python files with optional CLI arguments

## 🏗️ Architecture

### Agentic Loop

The core of Magnet AI is an **agentic loop** that allows the AI to make multiple function calls sequentially:

```python
for turn in range(max_turns):
    response = gemini.generate(messages)
    
    if response.has_function_calls:
        # Execute functions
        results = execute_functions(response.function_calls)
        
        # Add results to conversation
        messages.append(results)
        
        # Loop continues - AI decides next action
    else:
        # AI has final answer
        print(response.text)
        break
```

This pattern enables the AI to:
1. Call a function to list files
2. Read a specific file based on the listing
3. Modify the file
4. Run tests to verify changes
5. Provide a natural language summary

### Function Calling Pattern

Each function follows this pattern:

1. **Schema Definition** (`functions/schemas.py`): Defines the function signature for the AI
2. **Implementation** (`functions/*.py`): Actual Python function that performs the operation
3. **Routing** (`main.py`): Maps function calls to implementations
4. **Response Handling**: Sends results back to AI for next decision

## 📁 Project Structure

```
magnet-ai/
├── main.py                          # Entry point with agentic loop
├── config.py                        # System prompts and constants
├── tests.py                         # Unit tests for all functions
├── functions/
│   ├── get_files_info.py           # List directory contents
│   ├── get_file_content.py         # Read file with truncation
│   ├── write_file.py               # Write/update files (AI IDE pattern)
│   ├── run_python_file.py          # Execute Python scripts
│   └── schemas.py                  # Function declarations for Gemini
└── example_project_calculator/      # Example project for testing
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Poetry (for dependency management)
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/abderrahmanyouabd/magnet-ai.git
   cd magnet-ai
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   ```

### Usage

Run the AI agent with a prompt:

```bash
poetry run python main.py -p "what files are in the root?"
```

**With verbose output:**
```bash
poetry run python main.py -p "find main.py and run it" -v
```

**Limit function calling turns:**
```bash
poetry run python main.py -p "your prompt" --max-turns 5
```

### Example Commands

```bash
# List files in a directory
poetry run python main.py -p "what files are in the functions directory?"

# Read a file
poetry run python main.py -p "show me the content of config.py"

# Run a Python script
poetry run python main.py -p "run the calculator main.py file"

# Multi-step task
poetry run python main.py -p "find all Python files, read main.py, and tell me what it does"
```

## 🧪 Testing

Run the test suite:

```bash
poetry run python tests.py
```

## 🎓 Learning Resources

### Key Concepts Demonstrated

1. **Function Calling**: How to define and use tools with LLMs
2. **Agentic Loops**: Multi-turn conversations with function execution
3. **Security**: Path traversal prevention and input validation
4. **Line-Based Editing**: AI IDE-style code modification
5. **Subprocess Management**: Running external scripts safely

## 🤝 Contributing

This is a learning project, and contributions are welcome! Here's how you can help:

### Adding New Functions

1. **Create the function** in `functions/your_function.py`
   ```python
   def your_function(work_dir, ...):
       # Security checks
       # Implementation
       return result
   ```

2. **Define the schema** in `functions/schemas.py`
   ```python
   schema_your_function = types.FunctionDeclaration(
       name="your_function",
       description="What it does",
       parameters=types.Schema(...)
   )
   ```

3. **Add routing** in `main.py`
   ```python
   elif function_call_part.name == "your_function":
       result = your_function(...)
   ```

4. **Write tests** in `tests.py`
   ```python
   class TestYourFunction(unittest.TestCase):
       def test_your_function(self):
           # Test implementation
   ```

5. **Update system prompt** in `config.py`
   ```python
   SYSTEM_PROMPT = f"""
   ...
   - Your new capability description
   """
   ```

### Ideas for Contributions

- Add semantic code search
- Implement debugging tools
- Add code analysis functions
- Support for other languages
- Database integration
- Git operations
- Test generation
- Documentation generation

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run tests (`poetry run python tests.py`)
6. Commit your changes (`git commit -m '...'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Google Gemini API](https://ai.google.dev/)
- Inspired by [Cursor](https://cursor.sh/), [Windsurf](https://codeium.com/windsurf), and [GitHub Copilot](https://github.com/features/copilot)
- Created for educational purposes

**⭐ If you found this helpful for learning about AI agents, please star the repository!**
