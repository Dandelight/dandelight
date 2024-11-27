import os
from git import Repo
from datetime import datetime, timedelta
import json
import pytz

def get_local_timezone():
    return pytz.timezone('Asia/Shanghai')  # Replace with your local timezone

def analyze_git_history(repo_path='.'):
    repo = Repo(repo_path)
    local_tz = get_local_timezone()
    
    # Calculate yesterday's and today's 4:00 AM
    now = datetime.now(local_tz)
    today_4am = now.replace(hour=4, minute=0, second=0, microsecond=0)
    if now < today_4am:
        today_4am -= timedelta(days=1)
    yesterday_4am = today_4am - timedelta(days=1)
    
    lines_added = 0
    lines_deleted = 0

    for commit in repo.iter_commits(since=yesterday_4am, until=today_4am):
        for file in commit.stats.files.values():
            lines_added += file['insertions']
            lines_deleted += file['deletions']

    return lines_added, lines_deleted, yesterday_4am.date()

def main():
    added, deleted, report_date = analyze_git_history()
    
    data = {
        "date": report_date.strftime('%Y-%m-%d'),
        "added": added,
        "deleted": deleted
    }
    
    # Ensure the public directory exists
    os.makedirs('public', exist_ok=True)
    
    # Write to public/git_data.json
    with open('public/git_data.json', 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    main()

