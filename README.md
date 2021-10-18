add-msg-issue-suffix-hook
=========================

A prepare-commit-msg hook for pre-commit.
See also: https://github.com/pre-commit/pre-commit

This hook searches the branch's name for Jira issues and apends commit messages with it

### Install pre-commit

```bash
pip install pre-commit
```

### Install pre-commit-msg hook
Install prepare-commit-msg hooks using

```bash
pre-commit install --hook-type prepare-commit-msg
```

### Using with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/rnjesuz/add-msg-issue-suffix-hook
    rev: v0.1.0  # Use the ref you want to point at
    hooks:
    -   id: add-msg-issue-suffix
```

### Optional template argument
Change how the issue is rendered to the commit message using the `--template` argument.
Default is `[<issue name goes here>]`

```yaml
-   repo: https://github.com/rnjesuz/add-msg-issue-suffix-hook
    rev: v0.1.0  # Use the ref you want to point at
    hooks:
    -   id: add-msg-issue-suffix
        args:
            - --template=[{}]
```
