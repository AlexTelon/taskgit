# Taskgit

Taskgit is a in-file task manager for git repositories. Its designed to be checked in to your source code repository.
Comes with a set of commands to help you manage your tasks and a static webpage generator to visualize the current state of your tasks.

Since it is all text you can also yous recent advances in large language models to do things like mass modify tasks.

## Features

 - Small codebase (< 500 lines of code)
 - Integration to git by storing it in git
 - Text first interface
 - Powerful command line interface thanks to openai API's
 - Generate a static webpage to visualize your tasks


![taskgit sample image](sample.png)  
Example of the visual output taskgit generates. (yes its ugly for now)

### Using AI to update your tasks
While openai's api's are not free to use they are cheap. 
But you dont have to use them. Integrate your own or use github copilot when modifying/adding tasks directly in the tasks.toml file.

Here is an example of using the `taskgit bot` cli command.

```diff
# Let "chatgpt" modify your board with free text requests!
$ taskgit bot assign all tasks to Dondald Duck instead
# Using git diff to show the changes made
$ git diff tasks.toml
--- a/tasks.toml
+++ b/tasks.toml
@@ -7,7 +7,7 @@ hidden = ['backlog']
 id = 9
 title = "Generate githubpages with github actions"
 description = "Ideally the user should not have to generate it manually. It would be nice with a more generic solution however. Putting this on hold for now."
-assignee = "Alex Telon"
+assignee = "Donald Duck"
 column = "backlog"

 [[task]]
@@ -28,14 +28,14 @@ so that others can modify the code.

 Maybe not have a done/close column at all? We can ofc get it from history. But maybe it should only be visible in that view?
 """
-assignee = "Alex Telon"
+assignee = "Donald Duck"
 column = "todo"

 [[task]]
 id = 17
 title = "tasks can get too wide"
 description = "Long tasks can cause a column to take up like 50% of the screen."
-assignee = "Alex Telon"
+assignee = "Donald Duck"
 column = "todo"
...
```

```diff
$ taskgit bot add labels like ['bug', 'feature', 'idea'] to tasks. Also fix spelling errors

$ git diff tasks.toml
diff --git a/tasks.toml b/tasks.toml
index 3f20bab..d599f40 100644
--- a/tasks.toml
+++ b/tasks.toml
@@ -1,21 +1,17 @@
-[meta]
-order = ['todo', 'ongoing', 'done']
-hidden = ['backlog']
-
-
 [[task]]
 id = 9
-title = "Generate githubpages with github actions"
+title = "Generate github pages with github actions"
 description = "Ideally the user should not have to generate it manually. It would be nice with a more generic solution however. Putting this on hold for now."
 assignee = "Alex Telon"
 column = "backlog"
+labels = ["idea"]

 [[task]]
 id = 15
 title = "Figure out a nicer close process"
 description = """Should removing a task be considered closing it?

-In case you dont want to update the text as you close it you could just remove it in a commit.
+In case you don't want to update the text as you close it you could just remove it in a commit.

 But in case you want to update the text before you remove then right now you would first commit the
 change and then commit the removal..
@@ -26,10 +22,11 @@ But what of other types of removal like removed, deleted?
 I want to keep this simple yet flexible. So either make this configurable or make the code small and simple
 so that others can modify the code.

-Maybe not have a done/close column at all? We can ofc get it from history. But maybe it should only be visible in that view?
+Maybe not have a done/close column at all? We can of course get it from history. But maybe it should only be visible in that view?
 """
 assignee = "Alex Telon"
 column = "todo"
+labels = ["idea"]

 [[task]]
 id = 17
@@ -37,57 +34,63 @@ title = "tasks can get too wide"
 description = "Long tasks can cause a column to take up like 50% of the screen."
 assignee = "Alex Telon"
 column = "todo"
+labels = ["bug"]

 [[task]]
 id = 19
-title = "Detect if historic id's are reused and err"
+title = "Detect if historic ids are reused and err"
 description = """If one closes the last id from tasks.toml it is easy to forget that it has been used already. We should detect that and give an err.

-We need to store this information somewhere. I dont want to crawl all of git history to figure this out.
+We need to store this information somewhere. I don't want to crawl all of git history to figure this out.

 git merges are gonna be a problem...
 """
 assignee = "Alex Telon"
 column = "todo"
-
+labels = ["bug"]

 [[task]]
 id = 21
 title = "Rethink format and what this really is"
-description = """I mean this formfactor could mean we try things a little differently? Do we really need id's now that it is in git?
+description = """I mean this form factor could mean we try things a little differently? Do we really need ids now that it is in git?

-I dont know, but have a feeling there are interesting things here to explore.
+I don't know, but have a feeling there are interesting things here to explore.
 """
 assignee = "Alex Telon"
 column = "todo"
+labels = ["idea"]

 [[task]]
 id = 22
-title = "How to solve potential git merge conflicts with id's"
-description = """Should we skip Id's? Or should we have them but they are guids or something instead?
+title = "How to solve potential git merge conflicts with ids"
+description = """Should we skip Ids? Or should we have them but they are guids or something instead?

-But editing a file by hand would be harder. You would kindof have to use something like `taskgit add "title"` or `taskgit new` to create a template task with a guid to start with?"""
+But editing a file by hand would be harder. You would kind of have to use something like `taskgit add "title"` or `taskgit new` to create a template task with a guid to start with?"""
 assignee = "Alex Telon"
 column = "todo"
+labels = ["idea"]

 [[task]]
 id = 23
-title = "Improve err handling"
-description = "Right now it does not give line numbers and context for unexpexted errors"
+title = "Improve error handling"
+description = "Right now it does not give line numbers and context for unexpected errors"
 assignee = "Alex Telon"
 column = "todo"
+labels = ["bug"]

 [[task]]
 title = "Refactor generate_board_html"
 assignee = "Alex Telon"
 assignee = "Alex Telon"
 id = 24
 column = "ongoing"
+labels = ["feature"]

 [[task]]
 title = "taskgit modify <id> ..."
 assignee = "Alex Telon"
 id = 25
 column = "todo"
+labels = ["feature"]

 [[task]]
 title = "Nicer errors for unknown keys in toml"
@@ -99,10 +102,11 @@ description = """For now author is not a valid key for instance.
 assignee = "Alex Telon"
 id = 26
 column = "todo"
+labels = ["bug"]

 [[task]]
 title = "Investigate using ai to add/modify tasks"
-description = """For this to work well we need very good tooling that visualises what changed
+description = """For this to work well we need very good tooling that visualizes what changed

     taskgit update "Create a new task for each todo comment in the codebase"

@@ -113,14 +117,15 @@ description = """For this to work well we need very good tooling that visualises
     taskgit update "Remove all tasks in the done column"

 Some of these might be hard to do, the first one would require it to to know the codebase.
-But even if its only limited to the tasks.toml file itself it should be able to do these other things.
+But even if it's only limited to the tasks.toml file itself it should be able to do these other things.

-It could be used for individual tasks to. Like:
+It could be used for individual tasks too. Like:

     taskgit add "task for fixing the path bug on windows"

-But Im not sure that is a killer feature.
+But I'm not sure that is a killer feature.

 """
 id = 27
 column = "ongoing"
+labels = ["idea"]
\ No newline at end of file

# The output is not perfect, I would not have said id 24 is a 'feature', but out of the 3 example lables it was the closest one.
# The biggest issue is the removal of the meta information. But I think that is a temporary prompt issue on my part
# total tokens: 2211 which today costs 0.002 * 2.211 = 0.004422$. Or 226 requests per 1$.
```

The drawbacks of using the openai apis:
* You have to manually provide your own key
* It is not free
* It can get slow if you have a lot of tasks
* It might not work at all if you have lots of tasks

But again this is just one way of working with the text. I mosty edit things by hand in my editor.

## Installation

```bash
python -m pip install .
```

## Usage

```bash
# Create a tasks.toml
taskgit init

# This will generate a static webpage showing the tasks defined in tasks.toml.
# It will also open it for you in your default browser.
taskgit

# Create a minimal template for a task at the bottom.
taskgit add

# Use any and all args you can think of and it will write it to the task
taskgit add --title Improve err handling --description "Right now it does not give line numbers and context for unexpexted errors" --author "Alex Telon"

# But feel free to edit the text manually too!
```

## Task.toml

See the [tasks.toml](tasks.toml) file in this repository for an example.