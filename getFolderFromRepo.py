#!/usr/bin/python3
import requests
import warnings
import os

USERNAME: str = ''
TOKEN: str = ''
SHOW_INFO_LOGS: bool = True
SHOW_DEBUG_LOGS: bool = False

try:
    from config import *
except ImportError:
    pass

if len(USERNAME) == 0:
    env_username = os.environ.get('GITHUB_USERNAME', '')
    if env_username != '':
        USERNAME = env_username
    else:
        warnings.warn('GitHub Username not set')
if len(TOKEN) == 0:
    env_token = os.environ.get('GITHUB_TOKEN', '')
    if env_token != '':
        TOKEN = env_token
    else:
        warnings.warn('GitHub Token not set')


def decouple_url(url: str) -> dict:
    tmp_url = url
    tmp_url = tmp_url.strip('/') + str('/')
    tmp_url = tmp_url[tmp_url.index('github.com'):]
    tokens = tmp_url.split('/')
    if tokens[3] != '':
        branch = tokens[4]
        path = '/'.join(tokens[5:])
    else:
        branch = ''
        path = '/'

    return {'owner': tokens[1], 'repo': tokens[2], 'path': path, 'last_element': get_last_element(url), 'branch': branch}


def log(*args, is_debug: bool = False, **kwargs) -> None:
    if is_debug:
        if SHOW_DEBUG_LOGS:
            print('Debug:', *args, **kwargs)
    else:
        if SHOW_INFO_LOGS or SHOW_DEBUG_LOGS:
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


def get_item_from_repo(owner: str, repo: str, path: str, last_element: str, branch: str = '') -> None:
    proper_folder_path = proper_filepath(path)
    if proper_folder_path == '/':
        # TODO clone and exit (Take care of branch also)
        pass

    url = f'https://api.github.com/repos/{owner}/{repo}/contents{proper_folder_path}'
    if branch != '':
        url += f'?ref={branch}'
    log('Folder URL: ', url, is_debug=True)

    r = requests.get(url, auth=(USERNAME, TOKEN))
    data = r.json()
    if type(data) == dict:
        assert data['type'] == 'file'
        download_file(data['download_url'], data['path'], last_element)
    elif type(data) == list:
        for d in data:
            if d['type'] == 'file':
                download_file(d['download_url'], d['path'], last_element)
            elif d['type'] == 'dir':
                get_item_from_repo(
                    owner, repo, d['path'], last_element, branch)
            else:
                log(f'Incorrect type: {d["type"]}', is_debug=True)
                print('Sorry, an error occurred')
                exit(-1)


def download_file(url: str, path: str, last_element: str) -> None:
    new_path = get_new_path(path, last_element)
    log(f'Downloading file: {new_path}')

    log(f'Downloading file: {url}', is_debug=True)
    r = requests.get(url, auth=(USERNAME, TOKEN))
    log(f'Saving file: {new_path}', is_debug=True)
    if os.path.dirname(new_path):
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
    with open(new_path, 'wb+') as f:
        f.write(r.content)


def show_help():
    print(f"""USAGE:
    {__file__} <GitHub URL of the folder/file>
    """)


if __name__ == '__main__':
    def handle_url(url):
        try:
            url_details = decouple_url(url)

            log(f'Owner: {url_details["owner"]}', is_debug=True)
            log(f'Repo: {url_details["repo"]}', is_debug=True)
            log(f'Branch: {url_details["branch"]}', is_debug=True)
            log(f'Path: {url_details["path"]}', is_debug=True)
        except ValueError:
            print(f'{url} is not a valid GitHub Folder/File URL')
            show_help()
            exit(-1)
        get_item_from_repo(**url_details)

    import sys
    if len(sys.argv) == 2:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            show_help()
            exit()
        else:
            handle_url(sys.argv[1])
    elif len(sys.argv) > 2:
        for url in sys.argv[1:]:
            handle_url(url)
    else:
        show_help()
