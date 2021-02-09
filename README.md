add-msg-issue-prefix-hook
=========================

A prepare-commit-msg hook for pre-commit.

See also: https://github.com/pre-commit/pre-commit


### Using with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/avilaton/add-msg-issue-prefix-hook
    rev: v0.0.5  # Use the ref you want to point at
    hooks:
    -   id: add-msg-issue-prefix
```

and install prepare-commit-msg hooks using
```
pre-commit install --hook-type prepare-commit-msg
```

### Optional template argument
Change how the issue is rendered to the commit message using the `--template` argument.

```yaml
-   repo: https://github.com/avilaton/add-msg-issue-prefix-hook
    rev: v0.0.5  # Use the ref you want to point at
    hooks:
    -   id: add-msg-issue-prefix
        args:
            - --template=[{}]

```
