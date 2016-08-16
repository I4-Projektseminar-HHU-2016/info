# coding: utf-8

# run pip3 install github3.py==1.0.0a4 to get the correct version

import github3
# ask user for password (user must have access to the organization)
user, password = input("GitHub username: "), input("GitHub password: ")

# login using github3
g = github3.login(user, password=password)

# get the organization (e.g. "I4-Projektseminar-HHU-2016")
org_name = input("Enter GitHub organization to generate stats from: ")
o = g.organization(org_name)

# save stats in a list
stats = []

# iterate over all repositories for the given organization
for repo in o.repositories():
    # get stats for repo
    stat = list(repo.contributor_statistics())
    # get the user name and total commits (assuming there is only one
    # contributor)
    if len(stat) > 0:
        stats.append((stat[0].author.login, stat[0].total))

# sort the stats desc by commit count
stats.sort(key=lambda student: student[1], reverse=True)

# print the stats with a little bar chart (num_of_commits*"|")

print("\n##### Stats for organization {0} ###\n".format(org_name))
for stat in stats:
    print("{0}: {1} ({2})".format(stat[0], stat[1] * "|", stat[1]))

print()
