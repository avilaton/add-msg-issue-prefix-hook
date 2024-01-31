from add_msg_issue_prefix_hook import add_msg_issue_prefix
import re


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
        "task:TASK-1234 \n# Please enter the commit message for your changes."
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
