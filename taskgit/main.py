import argparse
import os
from pathlib import Path
import shutil
import traceback
import toml

import webbrowser

from taskgit.exceptions import KnownException
from taskgit.gen import generate_board_html
import taskgit.bot as bot


def init():
    # create a example task with named parameters
    example_tasks = [
        {"id": 1, "title": "Simple example"},
        {
            "id": 2,
            "title": "Larger example",
            "description": "Description here",
            "assignee": "Alex Telon",
            "column": "ongoing",
        },
    ]

    if os.path.exists("tasks.toml"):
        raise KnownException("tasks.toml file already exists!")
    else:
        with open("tasks.toml", "w", encoding="utf-8") as f:
            toml.dump({"task": example_tasks}, f)


def write_new_task(content):
    print("Adding task:")
    print(content.strip())

    # not super efficient to read this multiple times but fine for now.
    with open("tasks.toml", "r", encoding="utf-8") as f:
        ends_with_newline = f.read()[-1] == "\n"

    with open("tasks.toml", "a", encoding="utf-8") as f:
        if not ends_with_newline:
            content = "\n\n" + content
        f.write(content)


def add(**kwargs):
    """Add a line at the bottom of the taskgit.toml file with the correct format"""
    with open("tasks.toml", "r", encoding="utf-8") as f:
        tasks_data = toml.load(f)

    new_task = {k: v for k, v in kwargs.items() if v is not None}
    if "id" not in new_task:
        new_task["id"] = int(tasks_data["task"][-1]["id"]) + 1
    if "title" not in new_task:
        new_task["title"] = "Untitled"
    if "column" not in new_task:
        new_task["column"] = "todo"

    tasks_data["task"].append(new_task)

    with open("tasks.toml", "a", encoding="utf-8") as f:
        content = toml.dumps({"task": [new_task]})
        write_new_task(content)


def load_tasks(filename="tasks.toml"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return toml.load(f)
    except FileNotFoundError:
        raise KnownException(
            'tasks.toml file not found. Run "taskgit init" to create a new tasks.toml file.'
        )


def write_webpage(html):
    site_path = Path(".taskgit") / Path("site")
    site_path.mkdir(parents=True, exist_ok=True)

    html_path = site_path / "index.html"
    with html_path.open(mode="w", encoding="utf-8") as f:
        f.write(html)

    pkg_path = Path(__file__).resolve().parent
    shutil.copy(pkg_path / "style.css", site_path / "style.css")
    shutil.copy(pkg_path / "script.js", site_path / "script.js")


def open_webpage():
    webbrowser.open("file://" + os.path.realpath(".taskgit/site/index.html"))


def main():
    parser = argparse.ArgumentParser(
        prog="taskgit", description="A tool for managing tasks with git"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")
    subparsers.add_parser("init", help="Create a new tasks.toml file")
    subparsers.add_parser("add", help="Flexible cli for adding tasks. (write any and all --key value you wish)")
    subparsers.add_parser("bot", help="Ask openai to help you create/update tasks.")
    subparsers.add_parser("askbot", help="Ask openai to help you create/update tasks.")

    args, unknown_args = parser.parse_known_args()

    try:
        if args.command == "init":
            init()
            quit("Created tasks.toml file.")
        elif args.command == "add":
            kwargs = {}
            # pairwise go over --key value --key value
            for i in range(0, len(unknown_args), 2):
                key = unknown_args[i].lstrip("-")
                value = unknown_args[i + 1] if i + 1 < len(unknown_args) else ""
                kwargs[key] = value
            add(**kwargs)
        elif args.command == "bot":
            prompt = " ".join(unknown_args)
            response = bot.update_tasks(prompt)
            # TODO would be nice to not always overwrite everything.
            #      Doing so is costly and slow.
            #      Sometimes we just want to append a new task or edit one in place.
            with open("tasks.toml", "w", encoding="utf-8") as f:
                f.write(response)
        elif args.command == "askbot":
            prompt = " ".join(unknown_args)
            print(bot.ask(prompt))
        else:
            tasks = load_tasks()
            html = generate_board_html(tasks)
            write_webpage(html)
            open_webpage()

    except KnownException as e:
        quit(e)
    except Exception:
        traceback.print_exc()
        exit()


if __name__ == "__main__":
    main()
