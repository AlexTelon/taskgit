# Taskgit

Taskgit is a in-file task manager for git repositories. It uses git to track your tasks and history.  
You have the ability to generate a static webpage to visualize the current board. But editing is done in a task.toml file.

![taskgit sample image](sample.png)  
Example of the visual output taskgit generates.

## Installation

```bash
python -m pip install .
```

## Usage

```bash
# In a directory where you have a task.toml file
taskgit
# This will generate a static webpage in a .site/ directory and open it in your default browser.
```

## Task.toml

See the [task.toml](task.toml) file in this repository for an example.