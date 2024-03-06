import requests


def dag(qn, line=None):
    content = requests.get(
        "https://raw.githubusercontent.com/vinodhugat/qqqqq/main/"+qn)

    if line is not None:
        # If line parameter is provided
        modcontent = content.text.split("\n")  # Split content into lines
        # Extract start and end line numbers
        start, end = map(int, line.split("-"))
        # Select lines based on start and end
        selected_lines = modcontent[start-1:end]
        # Join selected lines into a single string
        return "\n".join(selected_lines)
    else:
        # If line parameter is not provided, return the entire content
        return content.text


