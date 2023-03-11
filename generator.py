import tomllib
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    title: str
    description: str = ''
    assignee: str = ''
    priority: int = None
    due_date: str = None
    done_date: str = None
    column: str = 'todo'
    
    def to_html(self):
        return """
        <div class="card" data-id="{}">
          <div class="title">#{} {}</div>
          <div class="description">{}</div>
          <div class="assignee">Assignee: {}</div>
          <div class="priority">Priority: {}</div>
          <div class="due-date">Due: {}</div>
        </div>
        """.format(self.id, self.id, self.title, self.description, self.assignee, self.priority or '', self.due_date or '')

# Read the tasks.toml file into a Python data structure
with open('tasks.toml', 'rb') as f:
    tasks_data = tomllib.load(f)

# Create a list of Task instances from the tasks data
tasks = [Task(**task_dict) for task_dict in tasks_data['task']]

# Define the HTML for the board and columns
board_html = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Task Board</title>
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
    <div class="board">
      <div class="column todo">
        <h2>Todo</h2>
        {}
      </div>
      <div class="column in-progress">
        <h2>In Progress</h2>
        {}
      </div>
      <div class="column done">
        <h2>Done</h2>
        {}
      </div>
    </div>
  </body>
</html>
"""

# Generate the HTML for each column
todo_html = "".join([task.to_html() for task in tasks if task.column == 'todo'])
in_progress_html = "".join([task.to_html() for task in tasks if task.column == 'in_progress'])
done_html = "".join([task.to_html() for task in tasks if task.column == 'done'])

# Sort the backlog and ongoing tasks by priority
tasks_by_column = {
    'todo': sorted([task for task in tasks if task.column == 'todo'], key=lambda task: task.priority or 0),
    'in_progress': sorted([task for task in tasks if task.column == 'in_progress'], key=lambda task: task.priority or 0)
}

# Sort the done tasks by date
tasks_by_column['done'] = sorted([task for task in tasks if task.column == 'done'], key=lambda task: task.done_date or '', reverse=True)

# Combine the column HTML into the board HTML
board_html = board_html.format(todo_html, in_progress_html, done_html)

# Write the HTML to a file
with open('site/board.html', 'w') as f:
    f.write(board_html)