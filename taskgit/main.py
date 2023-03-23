from collections import Counter
import os
import shutil
import sys
import toml
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
  try:
    with open('tasks.toml', 'r') as f:
        tasks_data = toml.load(f)
  except FileNotFoundError:
      quit('tasks.toml file not found. Run "taskgit init" to create a new tasks.toml file.')

  if 'task' not in tasks_data:
      quit('No tasks found in tasks.toml.')

  # Create a list of Task instances from the tasks data
  tasks = [Task(**task_dict) for task_dict in tasks_data['task']]

  # check tasks.id is unique.
  if any(duplicates := [id for id, count in Counter([task.id for task in tasks]).items() if count > 1]):
    quit(f"Duplicate task ids: {duplicates}")

  # Get the column order. If not specified, use the default order.
  column_order = tasks_data.get("column_order", {}).get("order", ['todo', 'ongoing', 'done'])

  # Get all unique columns from the tasks to a dict
  columns = {task.column:[] for task in tasks}

  missing_columns = columns.keys() - column_order
  if any(missing_columns):
      current = f"order = {column_order}"
      fixed = f"order = {column_order + list(missing_columns)}"
      hint = f"""Consider adding the following to your tasks.toml file:
[column_order]
{fixed}
{' ' * (len(current)+1) + '^' * (len(fixed) - len(current) - 1)}
      """
      quit(f"columns {list(missing_columns)} used but missing in olumn_order:\n" + hint)

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
      if name not in columns: return ''
      else: return f"""
      <div class="column {name}">
        <h2>{name.title()}</h2>
        {columns[name]}
      </div>
      """

  column_html = ''.join([generate_column_html(name) for name in column_order])

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
  if len(sys.argv) > 1 and sys.argv[1] == 'init':
    # create a example task wiht named parameters
    example_tasks = [
       {'id': 1, 'title':'Simple example' },
       {
       'id': 2,
       'title': 'Larger example',
       'description': 'Description here',
       'assignee': 'Alex Telon',
       'column': 'ongoing',
       }
    ]
    with open('tasks.toml', 'w') as f:
        toml.dump({'task': example_tasks}, f)
    quit('Created tasks.toml file.')

  # Create a .site directory.
  os.makedirs('.site', exist_ok=True)

  _generate_board_html()

  # copy the style.css file to the site directory
  shutil.copy('taskgit/style.css', '.site/style.css')

  webbrowser.open('file://' + os.path.realpath('.site/index.html'))


if __name__ == '__main__':
  main()