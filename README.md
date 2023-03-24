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
# Create a tasks.toml
taskgit init

# This will generate a static webpage showing the tasks defined in tasks.toml.
# It will also open it for you in your default browser.
taskgit

# Create a minimal template for a task at the bottom.
taskgit add

# Use any and all args you can think of and it will write it to the task
taskgit add --title Improve err handling --description "Right now it does not give line numbers and context for unexpexted errors" --author "Alex Telon"

# But feel free to edit the text manually too!
```

## Task.toml

See the [task.toml](task.toml) file in this repository for an example.