from collections import Counter
from dataclasses import dataclass
import re
from typing import List

from taskgit.exceptions import KnownException
import markdown

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    assignee: str = ""
    priority: int = None
    due_date: str = None
    done_date: str = None
    labels: List[str] = None
    column: str = "todo"

    def to_html(self):
        labels_html = ""
        if self.labels:
            labels_html = '<div class="row"><span>Labels:</span> '
            for label in self.labels:
                labels_html += f'<span class="meta-item label">{label}</span>'
            labels_html += "</div>"

        try:
            # Ensure that file links are relative to the root of the repo (and not .taskgit/site).
            description = re.sub(
                r"\[(.+)\]\((.+)\)",
                r"[\1](../../\2)",
                self.description,
            )
            description_html = markdown.markdown(description)
        except:
            description_html = self.description

        return f"""
        <div class="card" data-id="{self.id}">
          <div class="title"><span class="highlight">#{self.id}</span> {self.title}</div>
          <div class="description">{description_html}</div>
          <div class="meta">
            <div class="row"><span>Assignee:</span> <div class="meta-item assignee">{self.assignee}</div></div>
            {f'<div class="row"><span>Priority:</span> <div class="meta-item priority">{self.priority}</div></div>' if self.priority else ''}
            {f'<div class="row"><span>Due:</span> <div class="meta-item due-date">{self.due_date}</div></div>' if self.due_date else ''}
            {labels_html}
          </div>
        </div>
        """





def create_tasks(tasks_data: str) -> list[Task]:
    if "task" not in tasks_data:
        raise KnownException("No tasks found in tasks.toml.")

    # Create a list of Task instances from the tasks data
    return [Task(**task_dict) for task_dict in tasks_data["task"]]


def parse_meta(tasks_data: str) -> dict:
    # Get the column order. If not specified, use the default order.
    meta = tasks_data.get("meta", {})
    column_order = meta.get("order", ["todo", "ongoing", "done"])
    hidden_columns = meta.get("hidden", [])

    return {"order": column_order, "hidden": hidden_columns}


def validate_ids(tasks: list[Task]):
    # check tasks.id is unique.
    if any(
        duplicates := [
            id for id, count in Counter([task.id for task in tasks]).items() if count > 1
        ]
    ):
        raise KnownException(f"Duplicate task ids: {duplicates}")
    return tasks


def create_columns(tasks: list[Task], tasks_data: str) -> dict[str, list]:
    meta = parse_meta(tasks_data)
    hidden_columns = meta["hidden"]
    column_order = meta["order"]

    # Get all unique columns from the tasks to a dict
    columns = {task.column: [] for task in tasks if task.column not in hidden_columns}
    # sort columns on column_order
    columns = {col: columns[col] for col in column_order if col in columns}

    missing_columns = columns.keys() - column_order
    if any(missing_columns):
        current = f"order = {column_order}"
        fixed = f"order = {column_order + list(missing_columns)}"
        hint = f"""Consider adding the following to your tasks.toml file:
[column_order]
{fixed}
{' ' * (len(current)+1) + '^' * (len(fixed) - len(current) - 1)}
      """
        raise KnownException(
            f"columns {list(missing_columns)} used but missing in column_order:\n" + hint
        )
    return columns


def sort_tasks(tasks: list[Task], columns: dict[str, list]) -> dict[str, list[Task]]:
    for col in columns:
        _tasks = [task for task in tasks if task.column == col]
        if col == "done":
            # Sort the backlog and ongoing tasks by priority
            columns[col] = sorted(_tasks, key=lambda task: task.priority or "Low")
        else:
            # Sort the done tasks by date
            columns[col] = sorted(_tasks, key=lambda task: task.done_date or "", reverse=True)


def generate_board_html(tasks_data: str) -> str:
    """Generate the HTML for the board from the tasks data and returns a html string."""
    tasks = create_tasks(tasks_data)
    columns = create_columns(tasks, tasks_data)
    tasks = validate_ids(tasks)
    sort_tasks(tasks, columns)

    # Convert the tasks to HTML
    columns = {col: "".join([task.to_html() for task in tasks]) for col, tasks in columns.items()}

    # Generate column html.
    def generate_column_html(name):
        if name not in columns:
            return ""
        else:
            return f"""
      <div class="column {name}">
        <h2>{name.title()}</h2>
        {columns[name]}
      </div>
      """

    column_html = "".join([generate_column_html(name) for name in columns.keys()])

    board_html = f"""
  <!DOCTYPE html>
  <html>
    <head>
      <meta charset="UTF-8">
      <title>Task Board</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <div class="row">
        <button id="clear-filter" style="display: none;">Clear filter</button>
        <div id="current-filters"></div>
      </div>
      <div class="board">
        {column_html}
      </div>
      <script src="script.js"></script>
    </body>
  </html>
  """

    return board_html
