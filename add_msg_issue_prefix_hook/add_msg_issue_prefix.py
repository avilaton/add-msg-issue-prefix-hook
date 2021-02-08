#!/usr/bin/env python3

import sys
import re
import subprocess


def get_ticket_id_from_branch_name(branch):
    matches = re.findall('[a-zA-Z]{1,10}-[0-9]{1,5}', branch)
    if len(matches) > 0:
        return matches[0]


def main():
    commit_msg_filepath = sys.argv[1]

    branch = ""
    try:
        branch = subprocess.check_output(["git","symbolic-ref", "--short", "HEAD"], universal_newlines=True).strip()
    except Exception as e:
        print(e)

    result = get_ticket_id_from_branch_name(branch)
    issue_number = ""

    if result:
        issue_number = result.upper()

    with open(commit_msg_filepath, "r+") as f:
        content = f.read()
        content_subject = content.split("\n", maxsplit=1)[0].strip()
        f.seek(0, 0)
        if issue_number and issue_number not in content_subject:
            f.write("[{}] {}".format(issue_number, content))
        else:
            f.write(content)


if __name__ == "__main__":
    exit(main())
