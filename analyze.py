import argparse
import os


def dir_path(string):
    """
    Checks if a path is a directory
    :param string: Path to check
    :return: The path, if it is a directory, otherwise raises NotADirectoryError
    """
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def output_path(string):
    """
    Checks if a path doesn't exist
    :param string: Path to check
    :return: The path, if it doesn't exist, otherwise raises FileExistsError
    """
    if os.path.exists(string):
        raise FileExistsError(string)
    else:
        return string


def run():
    """
    Run the program
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", "-s", help="'MyData' folder from spotify data export", type=dir_path, required=True)
    parser.add_argument("--output", "-o", help="Output file", type=output_path, required=True)
    args = parser.parse_args()


if __name__ == "__main__":
    run()
