# Technology Stack

## Core Technologies
- **Python**: Main implementation language (3.9+)
- **CocoaPods**: iOS dependency management system that this tool helps create libraries for
- **Git**: Used for template repository management and version control

## Project Dependencies
- **argparse**: Command-line argument parsing
- No other external dependencies required for core functionality

## Build System
The project uses Python's setuptools for packaging and distribution.

## Installation Methods
1. **pipx** (recommended): `pipx install git+https://github.com/DargonLee/lee-devkit.git`
2. **Source installation**: Clone repo and run `pip3 install -e .`
3. **Install script**: Run `curl -fsSL https://github.com/DargonLee/lee-devkit/blob/main/install.sh | bash`

## Common Commands

### Installation
```bash
# Install with pipx
brew install pipx
pipx install git+https://github.com/DargonLee/lee-devkit.git

# Install from source
git clone https://github.com/DargonLee/lee-devkit.git
cd lee-devkit
pip3 install -e .
```

### Development Environment Setup
```bash
# Clone repository
git clone https://github.com/DargonLee/lee-devkit.git
cd lee-devkit

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .
```

### Usage Examples
```bash
# Create CocoaPods library with Example project
lee-devkit create MyLibrary

# Create CocoaPods library without Example project
lee-devkit create MyLibrary --no-example

# Configure author information
lee-devkit config --author "Your Name" --email "your@email.com"

# Show current configuration
lee-devkit config --show
```