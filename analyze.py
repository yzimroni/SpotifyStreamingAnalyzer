import argparse
import os
import utils
from spotify_streaming_analyzer import SpotifyStreamingAnalyzer
import json


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

    print("Scanning for streaming history files...")
    files = utils.get_streaming_history_files(args.source)
    print("Found %i streaming history files" % len(files))

    analyzer = SpotifyStreamingAnalyzer()
    for fn in files:
        with open(os.path.join(args.source, fn), mode="r", encoding="utf-8") as f:
            history = json.load(f)
            print("  == Loaded %i streaming records from %s" % (len(history), fn))
            analyzer.add_streaming_history(history)

    total_length = len(analyzer.get_streaming_history())
    print("Total streaming records: %i" % total_length)
    if total_length == 0:
        print("Streaming history is empty")
        return

    result = analyzer.analyze()
    result.to_csv(args.output)
    print("output written to %s" % args.output)



if __name__ == "__main__":
    run()
