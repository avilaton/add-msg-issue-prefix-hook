import add_msg_issue_prefix_hook
from add_msg_issue_prefix_hook import add_msg_issue_prefix
import re

def test_q():
    issue_number = "TASK-1234"
    content = "# Please enter the commit message for your changes. Lines starting\n# with '#' will be ignored, and an empty message aborts the commit."
    insert_after = re.compile("^")

    print(dir(add_msg_issue_prefix_hook))
    print(dir(add_msg_issue_prefix))
    assert 1 == 1
    result = add_msg_issue_prefix.modify_commit_message(content, issue_number, insert_after)
    print(result)
