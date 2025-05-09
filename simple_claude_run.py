#!/usr/bin/env -S uv run --script

import subprocess

task_path = "PRPs/test.yaml"

prompt = """

READ and understand fully {task_path} Think HARDER about the task and break it down into smaller steps. then EXECUTE the steps

"""

command = ["claude", "-p", prompt, "--dangerously-skip-permissions"]

process = subprocess.run(command, check=True)

print(f"Claude process exited with output: {process.stdout}")
