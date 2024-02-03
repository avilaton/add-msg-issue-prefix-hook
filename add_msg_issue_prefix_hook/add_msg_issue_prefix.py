#!/usr/bin/env python3

import argparse
import re
import subprocess


def get_ticket_id_from_branch_name(pattern: re.Pattern, branch: str) -> str:
    """
    Extracts the issue identifier from the branch name.

    Args
    ----
        pattern (re.Pattern): pattern to match the issue identifier
        branch (str): branch name

    Returns
    -------
        str or None: issue identifier if found, None otherwise

    """
    matches = re.findall(pattern, branch)
    if len(matches) > 0:
        return matches[0]


def modify_commit_message(content: str, issue_number: str, insert_after: re.Pattern) -> str:
    """
    Inserts the issue number into the commit message after the specified
    regex pattern.

    Args
    ----
        content (str): commit message contents
        issue_number (str): issue identifier to insert
        pattern (re.Pattern): pattern after which to insert the issue number

    Returns
    -------
        str: modified commit message

    """
    if match := re.search(insert_after, content):
        return match.group().strip() + issue_number.strip() + " " + content[match.end() :]

    return issue_number.strip() + " " + content


def has_tag(content_subject: str, template: str, pattern: str) -> bool:
    """
    Checks if the commit message already has a tag matching the template.

    Args
    ----
        content_subject (str): commit message subject
        template (str): template to match
        pattern (str): issue key pattern to match

    Returns
    -------
        bool: True if the commit message already has a tag, False otherwise

    """
    # Escape special characters in the template except for {}
    template = re.escape(template)
    template = template.replace(r"\{", "{").replace(r"\}", "}")

    template = template.format(pattern)
    return re.search(template, content_subject) is not None


DEFAULT_TEMPLATE = "[{}]"
DEFAULT_INSERT_AFTER = "^"
DEFAULT_PATTERN = "[a-zA-Z0-9]{1,10}-[0-9]{1,5}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("commit_msg_filepath")
    parser.add_argument(
        "-t",
        "--template",
        default=DEFAULT_TEMPLATE,
        help="Template to render ticket id into",
    )
    parser.add_argument(
        "-i",
        "--insert-after",
        default=DEFAULT_INSERT_AFTER,
        help="Regex pattern describing the text after which to insert the issue key.",  # noqa: E501
    )
    parser.add_argument(
        "-p",
        "--pattern",
        default=DEFAULT_PATTERN,
        help="Regex pattern describing the issue key.",
    )
    parser.add_argument(
        "-d",
        "--default",
        help="Default prefix if no issue is found",
    )

    args = parser.parse_args()
    commit_msg_filepath = args.commit_msg_filepath
    template = args.template
    default = args.default
    insert_after = re.compile(args.insert_after)
    pattern = re.compile(args.pattern)

    branch = ""
    try:
        branch = subprocess.check_output(
            ["git", "symbolic-ref", "--short", "HEAD"], universal_newlines=True
        ).strip()
    except Exception as e:
        print(e)

    if result := get_ticket_id_from_branch_name(pattern, branch):
        issue_number = result.upper()
    else:
        issue_number = ""

    with open(commit_msg_filepath, "r+") as f:
        content = f.read()
        content_subject = content.split("\n", maxsplit=1)[0].strip()
        tag_present = has_tag(content_subject, template, args.pattern)
        f.seek(0, 0)
        if issue_number and not tag_present:
            prefix = template.format(issue_number)
            new_msg = modify_commit_message(content, prefix, insert_after)
            f.write(new_msg)
        elif default and not tag_present:
            new_msg = modify_commit_message(content, default, insert_after)
            f.write(new_msg)
        else:
            f.write(content)


if __name__ == "__main__":
    exit(main())
