import os
import re


def get_streaming_history_files(directory):
    """
    Get all streaming history files from a directory
    :param directory: The directory to scan
    :return: A list containing all stream history files from the directory
    """
    r = re.compile(r"StreamingHistory\d{0,}\.json")
    history_files = list(filter(r.match, os.listdir(directory)))
    return history_files

