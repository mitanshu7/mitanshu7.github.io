# This script converts markdown files in the 'markdown' directory to HTML files in the 'html' directory using Pandoc.

# Import necessary libraries
import os
import subprocess
from glob import glob


# Function to convert markdown files to HTML using Pandoc
def convert_markdown_to_html(input_file: str, output_file: str, arguments: str = None):
    command = ["pandoc", input_file, "--output", output_file]

    if arguments:
        # If arguments is a string, split it into a list
        arguments = arguments.split(" ")
        command.extend(arguments)

    print(f"Converting {input_file} to {output_file} with command: {command}")

    # Check if pandoc is installed
    try:
        subprocess.run(["pandoc", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print(
            "Pandoc is not installed or not found in the system PATH. Please install Pandoc to use this script."
        )
        return

    # Run the pandoc command
    output = subprocess.run(
        args=command, check=True, capture_output=True, encoding="utf-8"
    )

    print(f"Command exited with {output.returncode} code, output: \n{output.stdout}")


###########################################################################################################

# Gather all markdown files in the 'markdown' directory
markdown_files = glob("markdown/*.md")
print(f"Found {len(markdown_files)} markdown files to convert.")

# Ensure the output directory exists
os.makedirs("html", exist_ok=True)

# Convert each markdown file to HTML
for markdown_file in markdown_files:
    # Determine the output file path
    output_file = markdown_file.replace("markdown/", "html/").replace(".md", ".html")

    # Special case for index.md
    if markdown_file == "markdown/index.md":
        # If the markdown file is 'markdown/index.md', output to 'index.html'
        output_file = "index.html"

        # Convert the markdown file to HTML without a template
        convert_markdown_to_html(markdown_file, output_file, arguments="--standalone")

    else:
        # Convert the markdown file to HTML
        convert_markdown_to_html(
            markdown_file,
            output_file,
            arguments="--standalone --template=html/template.html",
        )


# Print a completion message
print("All markdown files have been converted to HTML.")
