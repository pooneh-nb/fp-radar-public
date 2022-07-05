from datetime import datetime, timedelta
import requests
import git
from pprint import pprint


def get_commits(repo):
    """
    Give a repo, this function will return a list of commits since the last release.
    :param repo: a github repo.
    :return: array of commit messages.
    """

    # Get the last commit from the last release
    res = requests.get('https://api.github.com/repos/fingerprintjs/%s/tags' % repo)
    commit = res.json()[0].get('commit').get('sha')

    # Get the date of the last commit from the last release
    res = requests.get('https://api.github.com/repos/fingerprintjs/%s/commits/%s' % (repo, commit))
    date = res.json().get('commit').get('author').get('date')

    # Convert the date to a datetime and add 1 second to it,
    # So we don't get the last commit of the previous release.
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ") + timedelta(seconds=1)

    # Get all the commits messages since the last release
    res = requests.get('https://api.github.com/repos/fingerprintjs/%s/commits?since=%s' % (repo, date))
    a = [re.get('commit').get('message') for re in res.json()]
    return [re.get('commit').get('message') for re in res.json()]


def main():
    get_commits("fingerprintjs")


if __name__ == '__main__':
    main()
