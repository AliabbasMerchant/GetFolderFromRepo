from main import *


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


if __name__ == "__main__":
    test_proper_filepath()
