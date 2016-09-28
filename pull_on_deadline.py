# coding: utf-8

"""Pull from a list of Github repository URLs
and checkout the repositories to a given deadline."""

from git import Repo
import datetime
import os


def fetch_repos(repo_list):
    """Fetch all repositories from a given list (full Github URL each line)."""
    print("fetching repositories")
    with open(repo_list, "r") as inp:
        repos = list(inp)
    for repo in repos:
        repo_name = repo.rsplit("/")[-1].strip()
        repo = Repo.clone_from(repo.replace(
            "\n", ""), "./repos/{repo_name}".format(repo_name=repo_name))


def get_deadline():
    """Get deadline from stdin."""
    deadline_date = input(
        'Enter due date. E.g. 24.09.16   ').strip()
    deadline_time = input('Enter due time. E.g. 00:00   ').strip()
    utc_offset = input(
        "Enter your timezone (difference from UTC e.g. +0200 for CEST)   ")

    return datetime.datetime.strptime(
        deadline_date + deadline_time + utc_offset, "%d.%m.%y%H:%M%z")


def write_meta(infos, repo_path):
    """Add some meta info to each repo
    (for easier correction of the assignment)."""
    with open(os.path.join(repo_path, "info.txt"), "w") as output:
        output.write(str(infos))


def prepare_repo(deadline, repo_name, repo_path):
    """Checkout the repository to last commit within the deadline
    (assuming all work has been done in the master branch)."""
    latest_valid_commit = None
    repo = Repo(repo_path)
    infos = {'Github user': repo_name,
             'continued past deadline': False}

    # stop if there are no commits at all
    try:
        commits = repo.iter_commits()
    except ValueError:
        write_meta(infos, repo_path)
        return

    # reverse commits to iterate from oldest to newest
    for commit in reversed(list(commits)):
        if commit.authored_datetime <= deadline:
            latest_valid_commit = commit
        else:
            infos['continued past deadline'] = True
            infos['Last valid commit'] = (
                latest_valid_commit.message,
                latest_valid_commit.authored_datetime.strftime(
                    "%d.%m.%y %H:%M"))
            # checkout repo to the latest valid commit
            repo.git.checkout(latest_valid_commit)
            # write meta infos in repo dir
            write_meta(infos, repo_path)
            # stop loop since all further commits are not relevant anyway
            break


if __name__ == '__main__':

    fetch_repos(
        input("Enter filename of repository list (e.g. seminar-repos.txt)"))
    deadline = get_deadline()
    # iterate over all repositories
    for repo_name in os.listdir(os.path.join(os.curdir, "repos")):
        # ignore osx specific files TODO: handle this better!
        if repo_name != ".DS_Store":
            prepare_repo(deadline, repo_name, os.path.join(
                os.curdir, "repos", repo_name))
