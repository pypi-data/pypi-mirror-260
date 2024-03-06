# pathenger

pathenger is a utility package for Python, offering a straightforward way to determine the paths of executable files and temporary directories. It is especially useful for applications packaged with PyInstaller, facilitating access to crucial path information in different execution environments.

## Features

- **Executable Path Detection**: Easily retrieve the path of the executable file when your application is packaged with PyInstaller.
- **Temporary Directory Path**: Obtain the path to the temporary directory used by PyInstaller in one-file mode, allowing for efficient management of temporary files.
- **Versatile Application**: Useful in a variety of scenarios, from logging and file management to accessing resources bundled with your application.

## Installation

Install pathenger directly from PyPI to add it to your project:

```bash
pip install pathenger
```

## Usage

pathenger simplifies the process of getting the executable or script path, and the temporary directory path, especially for PyInstaller-packaged applications. Here's how to use it:

```python
from pathenger import *

# Get the path of the executable or script
executable_path = getExecutablePath()
print("Executable/Script Path:", executable_path)

# Get the path of the temporary directory (for PyInstaller one-file mode)
temp_path = getTempPath()
print("Temporary Directory Path:", temp_path)
```