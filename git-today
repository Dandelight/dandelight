#!usr/bin/env python

import os
import sys
from datetime import datetime, timedelta

import pytz
from git import Repo
from git.exc import InvalidGitRepositoryError
from rich.console import Console
from rich.table import Table


def get_local_timezone():
    return pytz.timezone("Asia/Shanghai")  # Replace with your local timezone


def find_git_repos(root_dir):
    git_repos = []
    for dirpath, dirnames, _ in os.walk(root_dir):
        if ".git" in dirnames:
            git_repos.append(dirpath)
            dirnames.remove(".git")  # Don't recurse into .git directories
    return git_repos


def analyze_git_history(repo_path="."):
    try:
        repo = Repo(repo_path)
    except InvalidGitRepositoryError:
        print(f"Invalid git repo: {repo_path}", file=sys.stderr)
        return {
            "name": os.path.basename(repo_path),
            "added": 0,
            "deleted": 0,
        }
    local_tz = get_local_timezone()

    # Calculate yesterday's and today's 4:00 AM
    now = datetime.now(local_tz)
    today = now.replace(hour=4, minute=0, second=0, microsecond=0)
    if now < today:
        today -= timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    lines_added = 0
    lines_deleted = 0

    for commit in repo.iter_commits(since=today, until=tomorrow):
        if not commit.author.email.endswith("@qingnan.tech"):
            continue

        for file in commit.stats.files.values():
            lines_added += file["insertions"]
            lines_deleted += file["deletions"]

    return {
        "name": os.path.basename(repo_path),
        "added": lines_added,
        "deleted": lines_deleted,
    }


def get_workspace_today_stats():
    workspace_dir = os.path.expanduser("~/workspace")
    repos = find_git_repos(workspace_dir)

    repo_data = []
    for repo_path in repos:
        repo_data.append(analyze_git_history(repo_path))

    data = {
        "date": datetime.now(get_local_timezone()).strftime("%Y-%m-%d"),
        "repos": repo_data,
    }

    return data


def main():
    data = get_workspace_today_stats()
    console = Console()

    # Create and configure the table
    table = Table(
        title=f"Work Today {data['date']}",
    )
    table.add_column("Repository", style="cyan")
    table.add_column("Added", justify="right", style="green")
    table.add_column("Deleted", justify="right", style="red")

    # Filter and add rows to the table
    for repo in data["repos"]:
        if repo["added"] != 0 or repo["deleted"] != 0:
            table.add_row(repo["name"], str(repo["added"]), str(repo["deleted"]))

    # Print the table
    console.print(table)


if __name__ == "__main__":
    main()
