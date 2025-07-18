# Design Document

## Overview

The Pod Repo Push feature extends the Lee DevKit tool with functionality to push CocoaPods libraries to spec repositories. This feature encapsulates the `pod repo push` command with configurable repositories and options, making it easier for developers to update their libraries.

The feature will be implemented as a new command module in the existing command structure of Lee DevKit, following the established patterns for command registration and execution.

## Architecture

The feature will follow the existing architecture of Lee DevKit:

1. **Command Module**: A new module `pod_repo_push.py` will be added to the `lee_devkit/commands` directory
2. **Configuration Integration**: The feature will use the existing configuration system to store and retrieve spec repository information
3. **Command Registration**: The module will register its command and arguments with the main scaffold
4. **Execution Flow**: The command will validate inputs, build the pod repo push command, and execute it

## Components and Interfaces

### 1. Command Module (`pod_repo_push.py`)

```python
# Main functions
def register_arguments(parser):
    # Register command arguments
    
def execute(args, config):
    # Execute the command
    
# Helper functions
def find_podspec_files():
    # Find podspec files in current directory
    
def validate_spec_repo(repo_name, config):
    # Validate if the spec repo exists in configuration
    
def build_push_command(repo_name, podspec_file, options):
    # Build the pod repo push command
    
def run_pod_command(command):
    # Execute the pod command and handle output
```

### 2. Configuration Extensions

The existing configuration system will be extended to support spec repositories:

```json
{
  "template_repo": "...",
  "author": "...",
  "email": "...",
  "organization": "...",
  "prefix": "...",
  "spec_repos": {
    "default": "NBSpecs",
    "repos": {
      "NBSpecs": "git@git.ninebot.com:iOS/NBSpecs.git",
      "OtherSpecs": "git@example.com:iOS/OtherSpecs.git"
    }
  }
}
```

### 3. Command Line Interface

The command will be accessible through the Lee DevKit CLI:

```
lee-devkit pod push [podspec_file] [--repo REPO_NAME] [options]
```

## Data Models

### SpecRepository

```python
class SpecRepository:
    """Represents a CocoaPods spec repository."""
    
    def __init__(self, name, url):
        self.name = name
        self.url = url
        
    @classmethod
    def from_config(cls, config, name):
        """Create a SpecRepository from configuration."""
        repos = config.get("spec_repos", {}).get("repos", {})
        url = repos.get(name)
        if not url:
            return None
        return cls(name, url)
        
    @classmethod
    def get_default(cls, config):
        """Get the default spec repository."""
        default_name = config.get("spec_repos", {}).get("default")
        if not default_name:
            return None
        return cls.from_config(config, default_name)
```

### PushOptions

```python
class PushOptions:
    """Options for pod repo push command."""
    
    def __init__(self):
        self.allow_warnings = True
        self.verbose = True
        self.skip_import_validation = True
        self.use_libraries = True
        self.use_modular_headers = True
        self.extra_args = []
        
    def to_args(self):
        """Convert options to command line arguments."""
        args = []
        if self.allow_warnings:
            args.append("--allow-warnings")
        if self.verbose:
            args.append("--verbose")
        if self.skip_import_validation:
            args.append("--skip-import-validation")
        if self.use_libraries:
            args.append("--use-libraries")
        if self.use_modular_headers:
            args.append("--use-modular-headers")
        args.extend(self.extra_args)
        return args
```

## Error Handling

The feature will handle the following error scenarios:

1. **No podspec file found**: Clear error message when no podspec file is found in the current directory
2. **Multiple podspec files**: Prompt the user to select one when multiple podspec files are found
3. **Invalid spec repository**: Error message when the specified repository is not configured
4. **Pod command failure**: Display the error output from the pod command and exit with non-zero status

## Testing Strategy

The feature will be tested with the following approaches:

1. **Unit Tests**:
   - Test finding podspec files in a directory
   - Test building the push command with different options
   - Test validation of spec repositories

2. **Integration Tests**:
   - Test the end-to-end flow with mock pod command execution
   - Test configuration loading and saving

3. **Manual Testing**:
   - Test with real podspec files and repositories
   - Test with different combinations of options