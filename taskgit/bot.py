import openai


def load_openai_key():
    if not openai.api_key:
        with open(".openai_key.secret", "r") as f:
            openai.api_key = f.read().strip()


PROBLEM_DOMAIN_DESCRIPTION = """\
You are a bot that given some instruction updates a tasks.toml file.
The file is used to generate a task board for a project.

{}

You may be asked to update existing tasks or add new ones. Provide correct toml for what the user requests.

question: {}
new contents of tasks.toml after your changes:
"""


def update_tasks(prompt):
    load_openai_key()
    with open("tasks.toml", "r", encoding="utf-8") as f:
        toml_content = f.read()
    prompt = PROBLEM_DOMAIN_DESCRIPTION.format(toml_content, prompt)

    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=2500,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response["choices"][0]["message"]["content"]


def ask(prompt):
    load_openai_key()
    with open("tasks.toml", "r", encoding="utf-8") as f:
        toml_content = f.read()

    prompt = f"""\
Context:

{toml_content}
question: {prompt}
"""

    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=2500,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response["choices"][0]["message"]["content"]
