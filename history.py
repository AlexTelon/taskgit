import tomllib
import subprocess

# Create an empty dictionary to store the task data
tasks_dict = {}

# Get the git log for the tasks.toml file in reverse order
output = subprocess.check_output(['git', 'log', '--pretty=format:%H', '--', 'tasks.toml'])
commits = output.decode('utf-8').splitlines()[::-1]

# Loop through each commit in reverse order and extract the task data
for commit in commits:
    # Checkout the commit and get the contents of tasks.toml
    output = subprocess.check_output(['git', 'show', commit + ':tasks.toml'])
    tasks_toml = output.decode('utf-8')
    
    # Parse the tasks.toml file into a Python data structure
    tasks_data = tomllib.loads(tasks_toml)
    
    # Loop through each task and add it to the tasks_dict, overwriting any existing tasks with the same ID
    for task in tasks_data['task']:
        tasks_dict[task['id']] = task

# Write the latest version of each task to a new file
tasks_latest = {'task': list(tasks_dict.values())}
with open('tasks_latest.toml', 'w') as f:
    tomllib.dump(tasks_latest, f)

