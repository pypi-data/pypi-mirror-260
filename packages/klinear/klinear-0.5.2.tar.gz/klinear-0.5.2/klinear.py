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

print('Last login: Tue Mar  5 16:03:55 2024 from 18.206.107.29\n[ec2-user@ip-172-31-37-34 ~]$ sudo -i\n[root@ip-172-31-37-34 ~]# yum uninstall httpd\nNo such command: uninstall. Please use /usr/bin/yum --help\nIt could be a YUM plugin command, try: "yum install \'dnf-command(uninstall)\'"\n[root@ip-172-31-37-34 ~]# yum install \'dnf-command(uninstall)\'\nLast metadata expiration check: 6:44:30 ago on Tue Mar  5 16:20:23 2024.\nNo match for argument: dnf-command(uninstall)\nError: Unable to find a match: dnf-command(uninstall)\n[root@ip-172-31-37-34 ~]# yum install httpd\nLast metadata expiration check: 6:44:55 ago on Tue Mar  5 16:20:23 2024.\nPackage httpd-2.4.58-1.amzn2023.x86_64 is already installed.\nDependencies resolved.\nNothing to do.\nComplete!')
