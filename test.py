from getFolderFromRepo import *


def test_proper_filepath():
    def is_valid_filepath(path: str) -> bool:
        # should start with /
        # should not end with /
        # so it should be / or /a or /a.../b
        assert path.startswith("/")
        if len(path) != 1:
            assert not path.endswith("/")
    paths = ["", "/", "/a", "/a/", "//", "a/b", "/a/b", "/a/b/"]
    for path in paths:
        proper_path = proper_filepath(path)
        print(path, proper_path, sep="\t\t")
        is_valid_filepath(proper_path)


def test_rel_path():
    import os
    for data in [
        ("https://github.com/owner/repo", "repo", "file", "repo/file"),
        ("https://github.com/owner/repo", "repo", "folder1/file", "repo/folder1/file"),
        ("https://github.com/owner/repo/tree/branch/folder1", "folder1", "folder1/file", "folder1/file"),
        ("https://github.com/owner/repo/tree/branch/folder1/folder2", "folder2", "folder1/folder2/file", "folder2/file"),
        ("https://github.com/owner/repo/blob/branch/folder1/folder2/file", "file", "folder1/folder2/file", "file"),
    ]:
        url, last_element, path, new_path = data
        assert get_last_element(url) == last_element
        assert get_new_path(path, last_element) == new_path


if __name__ == "__main__":
    test_proper_filepath()
    test_rel_path()
