#!/usr/bin/env python3
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import sys
import re
import subprocess


def main(argv=None):
    print("hello from hook")
    print(argv)

    commit_msg_filepath = sys.argv[1]

    branch = ""
    try:
        branch = subprocess.getoutput("git symbolic-ref --short HEAD").strip().upper()
    except Exception as e:
        print(e)
        pass

    regexp = r"(DR-|dr-)(.\d*)"

    result = re.search(regexp, branch)
    issue_number = ""

    if result:
        issue_number = result.group(0)

    with open(commit_msg_filepath, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        if issue_number:
            f.write("[{}] {}".format(issue_number, content))
        else:
            f.write(content)


if __name__ == "__main__":
    exit(main())
