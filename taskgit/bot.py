import openai

with open('.openai_key.secret', 'r') as f:
    openai.api_key = f.read().strip()

PROBLEM_DOMAIN_DESCRIPTION = """\
You are a bot that adds/deletes/updates tasks in a tasks.toml file.
The file is used to generate a task board for a project.

{}
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
    with open("tasks.toml", "r") as f:
        toml_content = f.read()
    prompt = PROBLEM_DOMAIN_DESCRIPTION.format(toml_content, prompt)

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