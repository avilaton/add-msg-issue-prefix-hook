#!/usr/bin/env python3

import argparse
import re
import subprocess


def get_issue_name_from_branch_name(branch):
    matches = re.findall('[a-zA-Z]{1,10}-[0-9]{1,5}', branch)
    if len(matches) > 0:
        return matches[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("commit_msg_filepath")
    parser.add_argument(
        '-t', '--template', default="[{}]",
        help='Template to render ticket id into',
    )
    args = parser.parse_args()
    commit_msg_filepath = args.commit_msg_filepath
    template = args.template

    branch = ""
    try:
        branch = subprocess.check_output(["git","symbolic-ref", "--short", "HEAD"], universal_newlines=True).strip()
    except Exception as e:
        print(e)

    issue_name = get_issue_name_from_branch_name(branch)

    with open(commit_msg_filepath, "r+") as f:
        content = f.read()
        content_subject = content.split("\n", maxsplit=1)[0].strip()
        f.seek(0, 0)
        if issue_name and issue_name not in content_subject:
            suffix = template.format(issue_name)
            f.write("{}\n\n {}".format(content, suffix))
        else:
            f.write(content)


if __name__ == "__main__":
    exit(main())
