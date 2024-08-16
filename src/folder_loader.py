from pathlib import Path
import os

EXECUTING_DIRECTORY = Path(__file__).parent.resolve()

# I hate how there isn't a function to just do this in python
def LoadFromFolder(Name):
	for File in os.listdir(EXECUTING_DIRECTORY / Name):
		if not File.endswith(".py"):
			continue

		if "__" in File:
			continue

		__import__(f"{Name}.{File[:-3]}", locals(), globals())
