# This script converts markdown files in the 'markdown' directory to HTML files in the 'html' directory using Pandoc.

# Import necessary libraries
import os
import re
import subprocess
from datetime import UTC, datetime
from glob import glob

# https://github.com/svpino/rfeed
from rfeed import Feed, Guid, Item

BASE_URL = "https://mitanshu7.github.io"


# Function to convert markdown files to HTML using Pandoc
def convert_markdown_to_html(input_file: str, output_file: str, arguments: str = None):
    command = ["pandoc", input_file, "--output", output_file, "--standalone"]

    if arguments:
        # If arguments is a string, split it into a list
        arguments = arguments.split(" ")
        command.extend(arguments)

    # print(f"Converting {input_file} to {output_file} with command: {command}")

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


def build_rss_item(markdown_file: str) -> Item:
    with open(markdown_file, "r", encoding="utf-8") as file:
        markdown_post = file.read()

    title = re.search(r"^title:(.+)", markdown_post, re.MULTILINE).group(1)
    link = f"{BASE_URL}/{markdown_file.replace('markdown/', 'html/').replace('.md', '.html')}"
    description = re.search(r"^description:(.+)", markdown_post, re.MULTILINE).group(1)
    date = re.search(r"^date:(.+)", markdown_post, re.MULTILINE).group(1)[3:-2]
    keywords = re.search(r"^keywords:(.+)", markdown_post, re.MULTILINE).group(1)[2:-1]
    categories = [keyword.strip(",").strip() for keyword in keywords.split(", ")]

    return Item(
        title=title,
        link=link,
        description=description,
        author="mitanshu.sukhwani@gmail.com (Mitanshu Sukhwani)",
        categories=categories,
        guid=Guid(link),
        pubDate=datetime.strptime(date, "%Y-%m-%d"),
    )


def build_rss_feed(rss_feed_items: list[Item]):
    feed = Feed(
        title="Mitanshu Sukhwani's Blog",
        link="https://mitanshu7.github.io/rss.xml",
        description="Hello, I’m Mitanshu Sukhwani, creator of PaperMatch with a Master’s in Physics from IIT Madras. I’ve worked at IISER Tirupati on EEG data, network science, and brain modeling. I enjoy exploring ML, Linux, and the intersection of neuroscience, software, and data.",
        language="en-US",
        lastBuildDate=datetime.now(UTC),
        items=rss_feed_items,
    )
    with open("rss.xml", "w", encoding="utf-8") as file:
        file.write(feed.rss())


###########################################################################################################

# Gather all markdown files in the 'markdown' directory
markdown_files = glob("markdown/*.md")
markdown_files.sort()
print(f"Found {len(markdown_files)} markdown files to convert.")

# Ensure the output directory exists
os.makedirs("html", exist_ok=True)

# List to contain rss feed items
rss_feed_items: list[Item] = []

# Convert each markdown file to HTML
for markdown_file in markdown_files:
    print(f"Processing {markdown_file}")
    # Determine the output file path
    output_file = markdown_file.replace("markdown/", "html/").replace(".md", ".html")

    # Special case for index.md
    if markdown_file == "markdown/index.md":
        # If the markdown file is 'markdown/index.md', output to 'index.html'
        output_file = "index.html"

        # Convert the markdown file to HTML without a template
        convert_markdown_to_html(markdown_file, output_file, arguments="")

    else:
        item = build_rss_item(markdown_file)
        rss_feed_items.append(item)

        # break
        # Convert the markdown file to HTML
        convert_markdown_to_html(
            markdown_file,
            output_file,
            arguments="--template=html/template.html --highlight-style=kate --mathjax",
        )

# Create rss.xml
build_rss_feed(rss_feed_items)

# Print a completion message
print("All markdown files have been converted to HTML.")
