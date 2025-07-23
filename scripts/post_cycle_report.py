#!/usr/bin/env python3
"""Post-cycle reporter: summarize merges in the last 24h and post to run log issue."""
import os
import subprocess
from datetime import datetime, timezone, timedelta
import requests


def get_merges() -> str:
    """Return formatted list of merges in the last 24 hours."""
    since_time = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    result = subprocess.run(
        [
            "git",
            "log",
            "--merges",
            f"--since={since_time}",
            "--pretty=format:%h %an - %s",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not lines:
        return "No merges in the last 24h."
    return "\n".join(f"- {line}" for line in lines)


def post_comment(issue_number: str, body: str) -> None:
    """Post `body` as a comment to the given issue via GitHub API."""
    token = os.environ["GITHUB_TOKEN"]
    repo = os.environ["GITHUB_REPOSITORY"]
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.post(url, headers=headers, json={"body": body})
    response.raise_for_status()


def main() -> None:
    issue = os.environ.get("RUN_LOG_ISSUE")
    if not issue:
        raise SystemExit("RUN_LOG_ISSUE env var not set")

    merges = get_merges()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    message = f"## Nightly Report ({now})\n### Recent merges\n{merges}\n"
    post_comment(issue, message)


if __name__ == "__main__":
    main()
