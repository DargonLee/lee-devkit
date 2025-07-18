# Project Structure

## Directory Organization

```
lee-devkit/
├── lee_devkit/              # Main package directory
│   ├── __init__.py          # Package initialization
│   ├── cli.py               # Command-line interface entry point
│   ├── scaffold.py          # Main scaffolding functionality
│   ├── config.py            # Configuration management
│   ├── commands/            # Command implementations
│   │   ├── __init__.py
│   │   ├── cocoapods.py     # CocoaPods library creation
│   │   ├── code_gen.py      # Code generation utilities
│   │   ├── file_tools.py    # File manipulation tools
│   │   ├── git_tools.py     # Git operations
│   │   └── project_init.py  # Project initialization
│   └── utils/               # Utility functions
│       ├── __init__.py
│       ├── file_ops.py      # File operations
│       ├── git_ops.py       # Git operations
│       ├── logger.py        # Logging functionality
│       └── text_ops.py      # Text processing utilities
├── template/                # Template directory for CocoaPods libraries
│   ├── NBTemplateModule/    # Template module structure
│   │   ├── Resources/       # Resources for the template
│   │   └── Sources/         # Source code for the template
│   ├── Example/             # Example project template
│   ├── NBTemplateModule.podspec  # Template podspec file
│   └── create_pod.sh        # Helper script for pod creation
├── tests/                   # Test directory
│   ├── __init__.py
│   ├── test_cli.py          # CLI tests
│   └── test_cocoapods.py    # CocoaPods functionality tests
├── setup.py                 # Package setup script
├── requirements.txt         # Project dependencies
├── install.sh               # Installation script
├── LICENSE                  # License file
└── README.md                # Project documentation
```

## Key Components

1. **Command Structure**:
   - The project uses a modular command system
   - Each command module in `lee_devkit/commands/` implements specific functionality
   - Commands are registered in `scaffold.py` and exposed through the CLI

2. **Template System**:
   - Templates are stored in the `template/` directory
   - `NBTemplateModule` is the base template that gets customized during project creation
   - Template includes both library structure and optional example project

3. **Configuration Management**:
   - User configuration stored in `~/.lee_devkit/config.json`
   - Includes author info, email, organization, and template repository URL

4. **Utility Functions**:
   - Common operations are abstracted in the `utils/` directory
   - Includes file operations, Git operations, logging, and text processing

## Code Organization Patterns

1. **Command Registration Pattern**:
   - Each command module implements `register_arguments()` and `execute()` functions
   - Main scaffold class dynamically loads and registers these commands

2. **Configuration Management**:
   - Central configuration with user overrides
   - Default values provided for all settings

3. **Template Processing**:
   - Templates are processed in a temporary directory before final placement
   - Processing includes renaming files/directories and replacing content