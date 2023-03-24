import toml
import subprocess

# Stores id: task dict
tasks_dict: dict[int, dict] = {}

output = subprocess.check_output(["git", "log", "--pretty=format:%H", "--", "tasks.toml"])
commits = output.decode("utf-8").splitlines()

# Loop through each commit in reverse order and extract the task data
for commit in commits[::-1]:
    # Checkout the commit and get the contents of tasks.toml
    output = subprocess.check_output(["git", "show", commit + ":tasks.toml"])
    tasks_data = toml.loads(output.decode("utf-8"))

    # Loop through each task and add it to the tasks_dict, overwriting any existing tasks with the same ID
    for task in tasks_data["task"]:
        tasks_dict[task["id"]] = task

# Write the latest version of each task to a new file
tasks_latest = {"task": list(tasks_dict.values())}
with open("tasks_latest.toml", "w") as f:
    toml.dump(tasks_latest, f)
