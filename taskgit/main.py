import argparse
import os
import shutil
import toml

import webbrowser

from .gen import generate_board_html


def main():
  parser = argparse.ArgumentParser(prog='taskgit', description='A tool for managing tasks with git')
  subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

  subparsers.add_parser('init', help='Create a new tasks.toml file')
  subparsers.add_parser('add',  help='Not implemented yet')

  args = parser.parse_args()

  if args.command == 'init':
    # create a example task with named parameters
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