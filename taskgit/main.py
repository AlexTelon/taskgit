import os
import shutil
import sys
import toml

import webbrowser

from .gen import generate_board_html


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

  try:
    with open('tasks.toml', 'r') as f:
        tasks_data = toml.load(f)
  except FileNotFoundError:
      quit('tasks.toml file not found. Run "taskgit init" to create a new tasks.toml file.')

  try:
    board_html = generate_board_html(tasks_data)
  except Exception as e:
    quit(e)

  with open('.site/index.html', 'w') as f:
        f.write(board_html)

  # copy the style.css file to the site directory
  pkg_path = os.path.dirname(os.path.abspath(__file__))
  shutil.copy(os.path.join(pkg_path, 'style.css'), '.site/style.css')

  webbrowser.open('file://' + os.path.realpath('.site/index.html'))


if __name__ == '__main__':
  main()