from datetime import datetime, timedelta
import requests


def get_commit_content(res):
    for rec in res:
        url = rec['html_url']
        commit_content = requests.get(rec['html_url'])


def get_commits(repo):

    """
    Give a repo, this function will return a list of commits since the last release.
    :param repo: a github repo.
    :return: array of commit messages.
    """

    # Get the last commit from the last release
    res = requests.get('https://api.github.com/repos/fingerprintjs/' + repo + '/commits?per_page=100').json()
    get_commit_content(res)
    a = 1
    while len(res) == 100:
        print(a)
        a += 1
        last_sha = res[99]['sha']
        res = requests.get('https://api.github.com/repos/fingerprintjs/' + repo + '/commits?per_page=100&sha=%s' %last_sha).json()
        get_commit_content(res)


    """for rec in res:
        print(rec["commit"])
    commit = res.json()[0].get('parents')"""




def main():
    get_commits("fingerprintjs")


if __name__ == '__main__':
    main()
