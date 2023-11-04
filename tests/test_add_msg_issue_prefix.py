import add_msg_issue_prefix_hook
from add_msg_issue_prefix_hook import add_msg_issue_prefix
import re

def test_modify_commit_message():
    issue_number = "TASK-1234"
    content = ("\n# Please enter the commit message for your changes."
    "Lines starting\n# with '#' will be ignored, and an empty message aborts the commit.\n")
    expected_result = issue_number + " " + content

    insert_after = re.compile("^")
    result = add_msg_issue_prefix.modify_commit_message(content, issue_number, insert_after)
    print(result)
    assert result == expected_result
