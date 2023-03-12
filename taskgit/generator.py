import os
import shutil
import tomllib
from dataclasses import dataclass
import webbrowser

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
        return f"""
        <div class="card" data-id="{self.id}">
          <div class="title">#{self.id} {self.title}</div>
          <div class="description">{self.description}</div>
          <div class="assignee">Assignee: {self.assignee}</div>
          {f'<div class="priority">Priority: {self.priority}</div>' if self.priority else ''}
          {f'<div class="due-date">Due: {self.due_date}</div>' if self.due_date else ''}
        </div>
        """

def _generate_board_html():
  with open('tasks.toml', 'rb') as f:
      tasks_data = tomllib.load(f)

  # Create a list of Task instances from the tasks data
  tasks = [Task(**task_dict) for task_dict in tasks_data['task']]

  # Get all unique columns from the tasks to a dict
  columns = {task.column:[] for task in tasks}
  
  for col in columns:
    _tasks = [task for task in tasks if task.column == col]
    if col == 'done':
      # Sort the backlog and ongoing tasks by priority
      columns[col] = sorted(_tasks, key=lambda task: task.priority or "Low")
    else:
      # Sort the done tasks by date
      columns[col] = sorted(_tasks, key=lambda task: task.done_date or '', reverse=True)

  # Convert the tasks to HTML
  columns = {col: ''.join([task.to_html() for task in tasks]) for col, tasks in columns.items()}

  # Generate column html.
  def generate_column_html(name):
      return f"""
      <div class="column {name}">
        <h2>{name.title()}</h2>
        {columns[name]}
      </div>
      """

  column_html = ''.join([generate_column_html(name) for name in columns])

  board_html = f"""
  <!DOCTYPE html>
  <html>
    <head>
      <meta charset="UTF-8">
      <title>Task Board</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <div class="board">
        {column_html}
      </div>
    </body>
  </html>
  """

  with open('.site/index.html', 'w') as f:
      f.write(board_html)

def main():

  # Create a .site directory.
  os.makedirs('.site', exist_ok=True)

  _generate_board_html()

  # copy the style.css file to the site directory
  shutil.copy('taskgit/style.css', '.site/style.css')

  webbrowser.open('file://' + os.path.realpath('.site/index.html'))


if __name__ == '__main__':
  main()