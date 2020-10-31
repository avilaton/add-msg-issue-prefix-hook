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
        branch = subprocess.getoutput("git symbolic-ref --short HEAD").strip()
    except Exception as e:
        print(e)
        pass

    print("branch: {}".format(branch))
    print("using new regex, ticket is: {}".format(get_ticket_id_from_branch_name(branch)))

    regexp = r"(DR-|dr-)(.\d*)"

    result = re.search(regexp, branch)
    issue_number = ""

    if result:
        issue_number = result.group(0).upper()

    with open(commit_msg_filepath, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        if issue_number:
            f.write("[{}] {}".format(issue_number, content))
        else:
            f.write(content)


if __name__ == "__main__":
    exit(main())
