import os

# Define the header to add
header_template = """---
layout: default
title: 
parent: readings
nav_order: 
---
"""

# Path to the directory containing your Markdown files
directory = "docs/readings"

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".md"):  # Process only Markdown files
        file_path = os.path.join(directory, filename)
        
        # Read the content of the file
        with open(file_path, "r") as file:
            content = file.read()

        # Check if the header already exists
        if content.startswith("---"):
            print(f"Header already exists in {filename}, skipping.")
            continue

        # Add the header to the top
        with open(file_path, "w") as file:
            file.write(header_template + "\n" + content)

        print(f"Added header to {filename}")
