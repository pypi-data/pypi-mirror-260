
# Contributing

## New Releases

To create a new release for PyPI, do the following:

1. Update the version number in `pyproject.toml` and commit to `main`.
2. Go to https://github.com/RelationalAI/relationalai-python/releases/new and create a new release with the same version number. You can create a new tag here with the "Choose a tag" dropdown. The version indicator should be in the format `vX.Y.Z`.
3. Fill in the release title (just the version number again) and description (a summary of the changes).
4. Click "Publish release".

That's it. A GitHub Action will automatically build and publish the new release to PyPI.

## Linting

You can lint using `ruff check` (assuming you've activated the virtual environment; otherwise `.venv/bin/ruff check`). You can also use `ruff check --fix` to attempt to fix the issues.

### Lint on Save

If you want to automatically lint your Python files on save, you can install the `Run on Save` extension by `emeraldwalk` and add the following configuration to a file called `.vscode/settings.json` in the project directory:

```json
{
    "emeraldwalk.runonsave": {
        "commands": [
            {
                "match": ".*\\.py$",
                "cmd": "${workspaceFolder}/.venv/bin/ruff check --fix ${file}",
                "isAsync": true
            }
        ]
    }
}
```

### Pre-commit Hook

You can also do this as a pre-commit hook (so that a lint check happens when you commit rather than when you save the file). To do this, add the following to a file called `.git/hooks/pre-commit` in the project directory:

```bash
#!/bin/sh

.venv/bin/ruff check $(git diff --cached --name-only --diff-filter=d | grep '\.py$')
```

Then do `chmod +x .git/hooks/pre-commit` to make the file executable.

Then if you attempt to make a commit with a Python file that doesn't pass the linting checks, the commit will be rejected. You can then do `ruff check --fix` to attempt to fix the issues.