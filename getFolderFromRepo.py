#!/usr/bin/python3
import requests
import warnings
import os

USERNAME = 'putYourGitHubUsernameHere'
TOKEN = 'putYourTokenHere'
DEBUG = False

try:
    from config import USERNAME, TOKEN, DEBUG
except ImportError:
    pass


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def proper_filepath(filepath: str) -> str:
    # should start with /
    # should not end with /
    # so it should be / or /a or /a.../b
    return '/' + filepath.strip('/')


def get_last_element(url: str) -> str:
    return url.strip('/')[url.rindex('/') + 1:]


def get_new_path(path: str, last_element: str) -> str:
    if last_element in path:
        return path[path.index(last_element):]
    else:
        return last_element + os.path.sep + path


def get_folder_from_repo(owner: str, repo: str, folder_path: str, last_element: str, branch: str = '', ):
    proper_folder_path = proper_filepath(folder_path)
    if proper_folder_path == '/':
        # TODO clone and exit (Take care of branch also)
        pass

    url = f'https://api.github.com/repos/{owner}/{repo}/contents{proper_folder_path}'
    if branch != '':
        url += f'?ref={branch}'
    debug('Folder URL: ', url)

    r = requests.get(url, auth=(USERNAME, TOKEN))
    data = r.json()
    if type(data) == type(dict()):
        assert data['type'] == 'file'
        download_file(data['download_url'], data['path'], last_element)
    elif type(data) == type(list()):
        for d in data:
            if d['type'] == 'file':
                download_file(d['download_url'], d['path'], last_element)
            elif d['type'] == 'dir':
                get_folder_from_repo(
                    owner, repo, d['path'], last_element, branch)
            else:
                print(f'Incorrect type: {d["type"]}')


def download_file(url: str, path: str, last_element: str) -> None:
    debug(f'Downloading file: {url}')
    print(f'Downloading file: {path}')

    new_path = get_new_path(path, last_element)
    if os.path.dirname(new_path):
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
    debug(f'Saving file: {new_path}')
    r = requests.get(url)
    with open(new_path, 'wb+') as f:
        f.write(r.content)


def show_help():
    print(f"""USAGE:
    {__file__} <GitHub URL of the folder/file>
    """)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            show_help()
            exit()
        try:
            URL = sys.argv[1]
            url = sys.argv[1].strip('/') + '/'
            url = url[url.index('github.com') + len('github.com') + 1:]
            owner = url[:url.index('/')]
            url = url[url.index('/') + 1:]
            repo = url[:url.index('/')]
            url = url[url.index('/'):]
            if url.startswith('/tree'):
                url = url[len('/tree/'):]
                branch = url[:url.index('/')]
                folder_path = url[url.index('/') + 1:]
            else:
                branch = ''
                folder_path = '/'
            debug(owner, repo, branch, folder_path, sep='\n')
        except ValueError:
            print('Please enter a valid GitHub Folder/File URL')
            show_help()
            exit(-1)
        get_folder_from_repo(owner, repo, folder_path,
                             get_last_element(URL), branch)
    else:
        show_help()
