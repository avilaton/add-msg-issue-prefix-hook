add-msg-issue-prefix-hook
=========================

A prepare-commit-msg hook for.

See also: https://github.com/pre-commit/pre-commit


### Using with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/avilaton/add-msg-issue-prefix-hook
    rev: v0.0.7  # Use the ref you want to point at
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
    rev: v0.0.7  # Use the ref you want to point at
    hooks:
    -   id: add-msg-issue-prefix
        args:
            - --template=[{}]

```

### Optional insert after argument

Customize where the issue key is inserted using regular expressions. The following example allows commit messages of the form `feat: add feature` to be updated to `feat: [ABC-123] add feature`.

```yaml
-   repo: https://github.com/avilaton/add-msg-issue-prefix-hook
    rev: v0.0.7  # Use the ref you want to point at
    hooks:
    - id: add-msg-issue-prefix
        name: add-msg-issue-prefix-test
        args: ["--insert-after", "^feat.?:|^fix.?:"]
```
