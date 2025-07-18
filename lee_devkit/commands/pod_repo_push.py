#!/usr/bin/env python3
"""
CocoaPods Repo Push Tool - Push podspec files to spec repositories
"""

import os
import subprocess
import glob
from pathlib import Path
from typing import Dict, List, Optional, Tuple

__version__ = "1.0.0"

def register_arguments(parser):
    """Register command arguments"""
    parser.add_argument('podspec', nargs='?', help='Path to the podspec file (optional, will auto-detect if not provided)')
    parser.add_argument('--repo', '-r', help='Spec repository name (uses default if not specified)')
    parser.add_argument('--no-allow-warnings', action='store_true', help='Disable --allow-warnings flag')
    parser.add_argument('--no-verbose', action='store_true', help='Disable --verbose flag')
    parser.add_argument('--no-skip-import-validation', action='store_true', help='Disable --skip-import-validation flag')
    parser.add_argument('--no-use-libraries', action='store_true', help='Disable --use-libraries flag')
    parser.add_argument('--no-use-modular-headers', action='store_true', help='Disable --use-modular-headers flag')
    parser.add_argument('--extra-args', help='Additional arguments to pass to pod repo push (comma-separated)')
    
    # Repository management
    repo_group = parser.add_argument_group('Repository Management')
    repo_group.add_argument('--list-repos', action='store_true', help='List configured spec repositories')
    repo_group.add_argument('--add-repo', nargs=2, metavar=('NAME', 'URL'), help='Add a new spec repository')
    repo_group.add_argument('--remove-repo', metavar='NAME', help='Remove a spec repository')
    repo_group.add_argument('--set-default-repo', metavar='NAME', help='Set the default spec repository')

def execute(args, config):
    """Execute the pod repo push command"""
    try:
        # Handle repository management commands first
        if hasattr(args, 'list_repos') and args.list_repos:
            return list_repositories(config)
        elif hasattr(args, 'add_repo') and args.add_repo:
            return add_repository(config, args.add_repo[0], args.add_repo[1])
        elif hasattr(args, 'remove_repo') and args.remove_repo:
            return remove_repository(config, args.remove_repo)
        elif hasattr(args, 'set_default_repo') and args.set_default_repo:
            return set_default_repository(config, args.set_default_repo)
        
        # Find podspec file if not provided
        podspec_file = args.podspec if hasattr(args, 'podspec') else None
        if not podspec_file:
            podspec_file = find_podspec_file()
            if not podspec_file:
                print("❌ No podspec file found in the current directory")
                print("Please specify a podspec file or run the command in a directory containing a .podspec file")
                return False
        
        # Validate podspec file
        if not validate_podspec_file(podspec_file):
            return False
        
        # Get repository
        repo_name = args.repo if hasattr(args, 'repo') else None
        if not repo_name:
            repo_name = get_default_repository(config)
            if not repo_name:
                print("❌ No default repository configured.")
                print("Use --repo to specify a repository or set a default with --set-default-repo")
                return False
        
        # Verify repository exists
        repo_url = get_repository_url(config, repo_name)
        if not repo_url:
            print(f"❌ Repository not found: {repo_name}")
            print("Available repositories:")
            list_repositories(config)
            print("Use --add-repo to add a new repository")
            return False
        
        # Create push options from arguments
        options = PushOptions.from_args(args)
        
        # Print summary
        print("\n📋 Push Summary:")
        print(f"  Podspec: {podspec_file}")
        print(f"  Repository: {repo_name} ({repo_url})")
        print("  Options:")
        for option, value in vars(options).items():
            if value and option != 'extra_args':
                print(f"    - {option}: {value}")
        if options.extra_args:
            print(f"  Extra Arguments: {', '.join(options.extra_args)}")
        print()
        
        # Confirm
        confirm = input("Continue with push? (Y/n): ")
        if confirm.lower() in ('n', 'no'):
            print("❌ Operation cancelled by user")
            return False
        
        # Build and execute command
        command = build_push_command(repo_name, podspec_file, options, repo_url)
        print(f"\n📦 Pushing {os.path.basename(podspec_file)} to {repo_name}...")
        
        return run_pod_command(command)
        
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        return False
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
        return False

def validate_podspec_file(podspec_file: str) -> bool:
    """Validate a podspec file"""
    # Check if file exists
    if not os.path.exists(podspec_file):
        print(f"❌ Podspec file not found: {podspec_file}")
        return False
    
    # Check if file is readable
    if not os.access(podspec_file, os.R_OK):
        print(f"❌ Cannot read podspec file: {podspec_file}")
        return False
    
    # Check file extension
    if not podspec_file.endswith(('.podspec', '.podspec.json')):
        print(f"⚠️ File does not have a .podspec or .podspec.json extension: {podspec_file}")
        confirm = input("Continue anyway? (y/n): ")
        if confirm.lower() != 'y':
            return False
    
    # Validate podspec with pod command
    print(f"🔍 Validating podspec file: {podspec_file}")
    try:
        result = subprocess.run(
            ["pod", "spec", "lint", "--quick", podspec_file],
            capture_output=True,
            text=True,
            check=False  # Don't raise exception on non-zero exit
        )
        
        if result.returncode == 0:
            print("✅ Podspec validation passed")
            return True
        else:
            print("⚠️ Podspec validation failed with warnings:")
            print(result.stderr)
            confirm = input("Continue anyway? (y/n): ")
            return confirm.lower() == 'y'
            
    except subprocess.SubprocessError as e:
        print(f"⚠️ Could not validate podspec: {e}")
        confirm = input("Continue anyway? (y/n): ")
        return confirm.lower() == 'y'

def find_podspec_file() -> Optional[str]:
    """Find a podspec file in the current directory"""
    # Look for both .podspec and .podspec.json files
    podspec_files = glob.glob("*.podspec") + glob.glob("*.podspec.json")
    
    if not podspec_files:
        print("❌ No podspec files found in the current directory")
        return None
    
    if len(podspec_files) == 1:
        print(f"📦 Found podspec file: {podspec_files[0]}")
        return podspec_files[0]
    
    # If multiple podspec files, ask the user to select one
    print("📋 Multiple podspec files found:")
    for i, file in enumerate(podspec_files):
        print(f"  {i+1}. {file}")
    
    while True:
        try:
            choice = input("Select a podspec file (number): ")
            index = int(choice) - 1
            if 0 <= index < len(podspec_files):
                selected_file = podspec_files[index]
                print(f"📦 Selected podspec file: {selected_file}")
                return selected_file
            print("❌ Invalid selection. Please try again.")
        except ValueError:
            print("❌ Please enter a number.")
        except KeyboardInterrupt:
            print("\n⚠️ Operation cancelled")
            return None

class PushOptions:
    """Options for pod repo push command"""
    
    def __init__(self):
        # Default options
        self.allow_warnings = True
        self.verbose = True
        self.skip_import_validation = True
        self.use_libraries = True
        self.use_modular_headers = True
        self.extra_args = []
        
        # Additional options
        self.swift_version = None
        self.sources = []
        self.no_overwrite = False
        self.local_only = False
        self.commit_message = None
    
    def to_args(self) -> List[str]:
        """Convert options to command line arguments"""
        args = []
        
        # Standard flags
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
        
        # Additional options
        if self.swift_version:
            args.extend(["--swift-version", self.swift_version])
        
        # Add sources
        for source in self.sources:
            args.extend(["--sources", source])
        
        # Other flags
        if self.no_overwrite:
            args.append("--no-overwrite")
        if self.local_only:
            args.append("--local-only")
        if self.commit_message:
            args.extend(["--commit-message", self.commit_message])
        
        # Extra arguments
        args.extend(self.extra_args)
        
        return args
    
    @classmethod
    def from_args(cls, args) -> 'PushOptions':
        """Create options from command line arguments"""
        options = cls()
        
        # Set options based on arguments
        options.allow_warnings = not args.no_allow_warnings
        options.verbose = not args.no_verbose
        options.skip_import_validation = not args.no_skip_import_validation
        options.use_libraries = not args.no_use_libraries
        options.use_modular_headers = not args.no_use_modular_headers
        
        # Parse extra arguments
        if args.extra_args:
            options.extra_args = args.extra_args.split(',')
        
        return options

def build_push_command(repo_name: str, podspec_file: str, options: PushOptions, repo_url: str) -> List[str]:
    """Build the pod repo push command"""
    # Start with the base command
    command = ["pod", "repo", "push", repo_name, podspec_file]
    
    # Add the repository URL to sources if not already included
    if repo_url not in options.sources:
        options.sources.append(repo_url)
    
    # Add all options
    command.extend(options.to_args())
    
    return command

def run_pod_command(command: List[str]) -> bool:
    """Execute the pod command and handle output"""
    print(f"🚀 Executing: {' '.join(command)}")
    print("⏳ This may take a while...")
    
    try:
        # Run the command with real-time output
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line buffered
            universal_newlines=True
        )
        
        # Process output in real-time
        stdout_lines = []
        stderr_lines = []
        
        # Function to read from a pipe and print lines
        def read_and_print(pipe, lines_list, prefix=""):
            for line in iter(pipe.readline, ''):
                if line:
                    print(f"{prefix}{line.rstrip()}")
                    lines_list.append(line)
            
        # Create threads to read stdout and stderr
        import threading
        stdout_thread = threading.Thread(
            target=read_and_print, 
            args=(process.stdout, stdout_lines)
        )
        stderr_thread = threading.Thread(
            target=read_and_print, 
            args=(process.stderr, stderr_lines, "⚠️ ")
        )
        
        # Start threads
        stdout_thread.start()
        stderr_thread.start()
        
        # Wait for process to complete
        exit_code = process.wait()
        
        # Wait for threads to complete
        stdout_thread.join()
        stderr_thread.join()
        
        # Close pipes
        process.stdout.close()
        process.stderr.close()
        
        # Check result
        if exit_code == 0:
            print("✅ Podspec pushed successfully")
            return True
        else:
            print(f"❌ Command failed with exit code {exit_code}")
            return False
            
    except subprocess.SubprocessError as e:
        print(f"❌ Failed to execute command: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        return False

# Repository management functions

def get_repositories(config) -> Dict[str, str]:
    """Get all configured repositories"""
    return config.get_spec_repos()

def get_default_repository(config) -> Optional[str]:
    """Get the default repository name"""
    return config.get_default_spec_repo()

def get_repository_url(config, name: str) -> Optional[str]:
    """Get the URL for a repository"""
    return config.get_spec_repo_url(name)

def list_repositories(config) -> bool:
    """List all configured repositories"""
    repos = get_repositories(config)
    default = get_default_repository(config)
    
    if not repos:
        print("📋 No repositories configured")
        return True
    
    print("📋 Configured repositories:")
    for name, url in repos.items():
        default_marker = " (default)" if name == default else ""
        print(f"  {name}: {url}{default_marker}")
    
    return True

def add_repository(config, name: str, url: str) -> bool:
    """Add a new repository"""
    # Validate URL format
    if not url.startswith(('http://', 'https://', 'git@', 'ssh://')):
        print(f"❌ Invalid repository URL format: {url}")
        print("URL should start with http://, https://, git@, or ssh://")
        return False
    
    # Add the repository
    success = config.add_spec_repo(name, url)
    
    if success:
        print(f"✅ Added repository: {name} ({url})")
        if config.get_default_spec_repo() == name:
            print(f"✅ Set {name} as the default repository")
    
    return success

def remove_repository(config, name: str) -> bool:
    """Remove a repository"""
    # Check if repository exists
    if not config.get_spec_repo_url(name):
        print(f"❌ Repository not found: {name}")
        return False
    
    # Check if this is the default repository
    is_default = config.get_default_spec_repo() == name
    
    # Remove the repository
    success = config.remove_spec_repo(name)
    
    if success:
        print(f"✅ Removed repository: {name}")
        if is_default:
            print(f"⚠️ Removed default repository. Please set a new default.")
    
    return success

def set_default_repository(config, name: str) -> bool:
    """Set the default repository"""
    # Check if repository exists
    if not config.get_spec_repo_url(name):
        print(f"❌ Repository not found: {name}")
        return False
    
    # Set the default repository
    success = config.set_default_spec_repo(name)
    
    if success:
        print(f"✅ Set {name} as the default repository")
    
    return success