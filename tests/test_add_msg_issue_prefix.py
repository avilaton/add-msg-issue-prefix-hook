import re

import pytest

from add_msg_issue_prefix_hook import add_msg_issue_prefix


def test_modify_commit_message_simple():
    issue_number = "TASK-1234"
    content = (
        "\n# Please enter the commit message for your changes."
        "Lines starting\n# with '#' will be ignored, and an empty message aborts the commit.\n"
    )
    expected_result = issue_number + " " + content
    insert_after = re.compile(add_msg_issue_prefix.DEFAULT_INSERT_AFTER)

    result = add_msg_issue_prefix.modify_commit_message(content, issue_number, insert_after)
    assert result == expected_result


def test_modify_commit_message_with_insert_after():
    issue_number = "TASK-1234"
    content = (
        "task:\n# Please enter the commit message for your changes."
        "Lines starting\n# with '#' will be ignored, and an empty message aborts the commit.\n"
    )
    expected_result = (
        "task: TASK-1234 \n# Please enter the commit message for your changes."
        "Lines starting\n# with '#' will be ignored, and an empty message aborts the commit.\n"
    )
    insert_after = re.compile("^task:")

    result = add_msg_issue_prefix.modify_commit_message(content, issue_number, insert_after)
    assert result == expected_result


def test_modify_commit_message_insert_after_not_found():
    issue_number = "TASK-1234"
    content = (
        "\n# Please enter the commit message for your changes."
        "Lines starting\n# with '#' will be ignored, and an empty message aborts the commit.\n"
    )
    expected_result = issue_number + " " + content
    insert_after = re.compile("^task:")

    result = add_msg_issue_prefix.modify_commit_message(content, issue_number, insert_after)
    assert result == expected_result


@pytest.mark.parametrize(
    "pattern, branch_name, expected_ticket_id",
    [
        (r"TASK-\d+", "feature/TASK-1234-add-new-feature", "TASK-1234"),  # simple match
        (r"TASK-\d+", "feature/add-new-feature", None),  # no match
        (r"TASK-\d+", "feature/TASK-1234-and-TASK-5678", "TASK-1234"),  # first match
    ],
)
def test_get_ticket_id_from_branch_name_basic_parametrized(
    pattern, branch_name, expected_ticket_id
):
    """
    Parametrized test for the extraction of a ticket ID from a branch name.

    It tests for the correct handling of basic regex patterns, to ensure the correct match
    (the first one) is returned.
    """
    ticket_id = add_msg_issue_prefix.get_ticket_id_from_branch_name(
        pattern=pattern, branch=branch_name
    )
    assert ticket_id == expected_ticket_id, (
        f"Failed for pattern: {pattern}, branch_name: {branch_name}, getting wrong ticket_id: {ticket_id}"
    )


@pytest.mark.parametrize(
    "pattern, branch_name, expected_ticket_id",
    [
        (  # two groups
            r"(TASK-\d+)|(BUG-\d+)",
            "feature/TASK-1234-add-new-feature",
            "TASK-1234",
        ),
        (  # two groups, match the second
            r"(TASK-\d+)|(BUG-\d+)",
            "bugfix/BUG-1234-add-new-feature",
            "BUG-1234",
        ),
        (  # one group and additional part without group
            r"(TASK|BUG|FEATURE)-\d+",
            "feature/FEATURE-1234-add-new-feature",
            "FEATURE-1234",
        ),
        (  # regex with lookahead
            r"(?<=feature/)(TASK|BUG)-\d+",
            "feature/TASK-9999-add-new-feature",
            "TASK-9999",
        ),
        (  # nested groups
            r"((?<=feature/)(TASK|BUG|FEATURE)-\d+)",
            "feature/FEATURE-1234-add-new-feature",
            "FEATURE-1234",
        ),
    ],
)
def test_get_ticket_id_from_branch_name_using_regex_groups_parametrized(
    pattern, branch_name, expected_ticket_id
):
    """
    Parametrized test for the extraction of a ticket ID from a branch name.

    It tests for the correct handling of regex patterns containing one or more groups.
    """

    ticket_id = add_msg_issue_prefix.get_ticket_id_from_branch_name(
        pattern=pattern, branch=branch_name
    )
    assert ticket_id == expected_ticket_id, (
        f"Failed for pattern: {pattern}, branch_name: {branch_name}, getting wrong ticket_id: {ticket_id}"
    )
