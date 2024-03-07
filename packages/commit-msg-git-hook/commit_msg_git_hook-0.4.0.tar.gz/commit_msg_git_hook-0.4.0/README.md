# Commit Message Git Hook

A set of tools to validate git Conventional Commit messages.

See the [Conventional Commits Specification](https://www.conventionalcommits.org/en/v1.0.0/).

**NOTE**: It doesn't affect any previous commit on your repository.

## Installation Instructions

### Install from PyPI (Python Package Index)

Run the script below to install the latest version of this package:

```bash
pip install commit-msg-git-hook --upgrade
```

### Setup the Local Git Hook `commit-msg`

Run one of the scripts below to scaffold the hook:

- For Linux and macOS:
```bash
python3 -m commit_msg_git_hook.setup
```

- For Windows:
```bash
python -m commit_msg_git_hook.setup
```

It does the following steps:

- Reads and then shows the type of your Operating System.
    - Exits with an error message if the OS is unsupported.
- Creates a directory for git-hooks, by default `./.github/git-hooks`.
    - Creates subdirectories for each of the supported OS's.
    - Creates the `commit-msg` hook file for each OS if it doesn't exist.
        - Fills it with a basic script to call `commit_msg.main()`, from this package.
        - If the OS is Linux or macOS, makes the hook file executable.
- Sets the hooks (relative) path to the current repository as the directory respective to the OS type (for example: `./.github/git-hooks/linux`).
- Creates a configuration file `commit-msg.config.json` if it doesn't exist.
- Ends with a success message referencing again the type of your OS.

## Configuration Instructions

Customize the configuration file `commit-msg.config.json` to fit your project's needs.

Probably you will want to add **scopes**, to fully utilize the [Conventional Commits Specification](https://www.conventionalcommits.org/en/v1.0.0/).

## Basic Usage

After setting up and adding the new files to your git remote repository, your collaborators will
need to run the **installation** and **setup** steps again.
But, this time, the setup will only set the hooks path and make sure the file `commit-msg` is
executable.

Every time you make a commit, the hook will check if its message is in accordance to the
specification and the project's customization.

## How To Edit Commits

If your branch is not shared yet (not merged into `develop`, for example), you can edit your commits
with the command below. Git will list the last `n` commits and ask you whether you want to keep or
edit each one of them.

```bash
git rebase -i HEAD~n
```

More information here: https://docs.github.com/pt/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/changing-a-commit-message

## Credits

This package was created from a **Craicoverflow** tutorial.

See the tutorial at the link:
https://dev.to/craicoverflow/enforcing-conventional-commits-using-git-hooks-1o5p