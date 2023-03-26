import openai

with open('.openai_key.secret', 'r') as f:
    openai.api_key = f.read().strip()

PROBLEM_DOMAIN_DESCRIPTION = """\
You are a bot that adds/deletes/updates tasks in a tasks.toml file.
The file is used to generate a task board for a project.

[meta]
order = ['todo', 'ongoing', 'done']
hidden = ['backlog']

[[task]]
# Id should be unique
id = 9
# Title is mandatory
title = "Title of the task"
description = "Description of the task here"
assignee = "author name here"
# The columns should be one of the ones defined in the meta section
# column is mandatory
column = "backlog

The comments above are for your benefit, dont generate comments in your response.

You may be asked to update existing tasks or add new ones. Provide correct toml for what the user requests.

Just provide the new/updated tasks for the file.

Examples:

question: "Add a new task"
response:
[[task]]
id = 10
title = "New task"
column = "todo"

question: "Make Donald Duck the assignee of task 10"
response:
[[task]]
id = 10
title = "New task"
assignee = "Donald Duck"
column = "todo"

Now comes the actual question:

question: {}
response: 
"""

def ask(prompt):
    prompt = PROBLEM_DOMAIN_DESCRIPTION.format(prompt)

    # TODO try out text-davinci-edit-001 for edit tasks
    # TODO how to handle removal of tasks?
    # TODO try different models

    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5
    )

    return completions.choices[0].text.strip()