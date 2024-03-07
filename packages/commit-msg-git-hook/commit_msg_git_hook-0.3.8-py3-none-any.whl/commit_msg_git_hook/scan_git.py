from commit_msg_git_hook import commit_msg as cm
import subprocess
import sys

old_commit_sha = sys.argv[1]
new_commit_sha = sys.argv[2]

commit_shas = subprocess.run(
    [f"git rev-list {old_commit_sha}..{new_commit_sha}"],
    shell=True,
    capture_output=True,
    text=True,
).stdout.rstrip("\n").split("\n")

for commit_sha in commit_shas:
    msg_first_line = subprocess.run(
        [f"git cat-file commit {commit_sha} | sed '1,/^$/d'"],
        shell=True,
        capture_output=True,
        text=True,
    ).stdout.rstrip("\n").split("\n")[0]

    cm.main(msg_first_line)
exit(0)
