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
        from pprint import pprint
        pprint(*args, **kwargs)


def main():
    owner = input('Please enter the repo owner name: ')
    if owner == '':
        print('Owner cannot be empty')
        exit(1)
    repo = input('Please enter the repo name: ')
    if repo == '':
        print('Repo cannot be empty')
        exit(1)
    branch = input('Please enter the branch name (default: repo\'s default branch): ')
    folder_path = input('Please enter the folder path (default: /): ')
    get_folder_from_repo(owner, repo, branch, folder_path)


def get_folder_from_repo(owner: str, repo: str, branch: str = '', folder_path: str = '/'):
    folder_path = proper_filepath(folder_path)
    if folder_path == '/':
        # TODO clone and exit (Take care of branch also)
        pass
    
    url = f'https://api.github.com/repos/{owner}/{repo}/contents{folder_path}'
    if branch != '':
        url += f'?ref={branch}'
    debug(url)

    r = requests.get(url, auth=(USERNAME, TOKEN))
    data = r.json()
    if type(data) == type(dict()):
        assert data['type'] == 'file'
        download_file(data['download_url'], data['path'])
    elif type(data) == type(list()):
        for d in data:
            if d['type'] == 'file':
                download_file(d['download_url'], d['path'])
            elif d['type'] == 'dir':
                get_folder_from_repo(owner, repo, branch, d['path'])
            else:
                print(f'Incorrect type: {d["type"]}')


def proper_filepath(filepath: str) -> str:
    # should start with /
    # should not end with /
    # so it should be / or /a or /a.../b
    return '/' + filepath.strip('/')

def download_file(url: str, path: str) -> None:
    debug(f'Downloading file: {url}')
    print(f'Downloading file: {path}')

    proper_path = proper_filepath(path)[1:]
    
    if proper_path.startswith('..' + os.path.sep) or proper_path.startswith(os.path.sep):
        warnings.warn(f'Error in path. Skipping the file: {path}')
        debug(f'Path: {proper_path}')
    else:
        if os.path.dirname(proper_path):
            os.makedirs(os.path.dirname(proper_path), exist_ok=True)
        r = requests.get(url)
        with open(proper_path, 'wb+') as f:
            f.write(r.content)


if __name__ == '__main__':
    import sys
    if sys.argv[1]:
        try:
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
            # print(owner, repo, branch, folder_path, sep='\n')
        except ValueError:
            print('Please enter a valid GitHub URL')
            exit(-1)
        get_folder_from_repo(owner, repo, branch, folder_path)
    else:
        main()
