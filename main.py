import requests
import warnings

USERNAME = "putYourGitHubUsernameHere"
TOKEN = "putYourTokenHere"

try:
    from config import USERNAME, TOKEN
except ImportError:
    pass


def debug(*args, **kwargs):
    print(*args, **kwargs)


def main():
    global initial_path
    owner = input("Please enter the repo owner name:")
    if owner == "":
        print("Owner cannot be empty")
        exit(1)
    repo = input("Please enter the repo name:")
    if repo == "":
        print("Repo cannot be empty")
        exit(1)
    branch = input(
        "Please enter the branch name (default: repo's default branch):")
    folder_path = input("Please enter the folder path (default: /):")
    # TODO direct clone if empty
    folder_path = proper_filepath(folder_path)
    initial_path = folder_path
    get_folder_from_repo(owner, repo, branch, folder_path)


def get_folder_from_repo(owner, repo, branch="", folder_path="/"):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents{folder_path}"
    if branch != "":
        url += f"?ref={branch}"
    debug(url)

    r = requests.get(url, auth=(USERNAME, TOKEN))
    data = r.json()
    if type(data) == type(dict()):
        assert data['type'] == "file"
        download_file(data['download_url'], data['path'])
    elif type(data) == type(list()):
        for d in data:
            if d['type'] == 'file':
                download_file(d['download_url'], d['path'])
            elif d['type'] == 'dir':
                get_folder_from_repo(owner, repo, branch, "/"+d['path'])
            else:
                print(f'Incorrect type: {d["type"]}')


def proper_filepath(filepath: str) -> str:
    # should start with /
    # should not end with /
    # so it should be / or /a or /a.../b
    return "/" + filepath.strip('/')


def download_file(url, path):
    global initial_path
    import pathlib
    import os

    debug(f'Downloading file: {url}')
    print(f'Downloading file: {path}')

    proper_path = proper_filepath(path)
    proper_intial = proper_filepath(initial_path)
    if (proper_path).startswith(proper_intial):
        new_path = os.path.relpath(proper_path, start=proper_intial)
    else:
        warnings.warn("Error in path")
        debug(f'InitialPath={proper_intial}, Path={new_path}')

    print(f'Downloading file: {new_path}')
    if new_path.startswith('..' + os.path.sep) or new_path.startswith(os.path.sep):
        warnings.warn("Error in path. Skipping the file: path")
        debug(f'ProperPath: {new_path}')
    else:
        if os.path.dirname(new_path):
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
        r = requests.get(url)
        with open(new_path, 'wb+') as f:
            f.write(r.content)


if __name__ == "__main__":
    initial_path = "/"
    # di0002ya/ESS/tree/master/data/NASA
    # get_folder_from_repo("AliabbasMerchant",
    #                      "SecureNotes", "", "/")
    get_folder_from_repo("di0002ya",
                         "ESS", "", "/data/NASA")
