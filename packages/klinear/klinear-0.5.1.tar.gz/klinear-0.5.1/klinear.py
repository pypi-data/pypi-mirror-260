import requests

def dag(qn, line=None):
    content = requests.get("https://raw.githubusercontent.com/vinodhugat/qqqqq/main/"+qn)

    if line is not None:
        # If line parameter is provided
        modcontent = content.text.split("\n")  # Split content into lines
        start, end = map(int, line.split("-"))  # Extract start and end line numbers
        selected_lines = modcontent[start-1:end]  # Select lines based on start and end
        return "\n".join(selected_lines)  # Join selected lines into a single string
    else:
        # If line parameter is not provided, return the entire content
        return content.text

print(dag("01","1-5"))