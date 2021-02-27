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


def run():
    """
    Run the program
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", "-s", help="'MyData' folder from Spotify data export", type=dir_path, required=True)
    parser.add_argument("--output", "-o", help="Output file", type=str, required=True)
    parser.add_argument("--from-date", "-d", help="Optional. Filter streaming history before this date (format: "
                                                  "YYYY-MM-DD)", type=str)
    parser.add_argument("--min-count", "-c", help="Optional. Filter songs below a specific play count", type=int)

    args = parser.parse_args()

    print("Scanning for streaming history files...")
    files = utils.get_streaming_history_files(args.source)
    print("Found %i streaming history files" % len(files))

    analyzer = SpotifyStreamingAnalyzer()
    for fn in files:
        # Load each streaming history file as json
        with open(os.path.join(args.source, fn), mode="r", encoding="utf-8") as f:
            history = json.load(f)
            print("  == Loaded %i streaming records from %s" % (len(history), fn))
            # Add streaming history records to analyzer
            analyzer.add_streaming_history(history)

    analyzer.generate_data_frame()

    # Filter streaming history by date
    if args.from_date:
        print("Filtering streaming history before %s" % args.from_date)
        analyzer.filter_by_date(args.from_date)

    total_length = analyzer.get_data_frame().size
    print("Total streaming records: %i" % total_length)
    if total_length == 0:
        # If length is 0, we have no records to analyze
        print("Streaming history is empty")
        return

    analyzer.analyze()

    # Filter songs below specified play count
    if args.min_count:
        print("Filtering songs with play count less than %i" % args.min_count)
        analyzer.filter_by_play_count(args.min_count)

    result = analyzer.get_result()
    # Save results to file
    result.to_csv(args.output)
    print("Output written to %s" % args.output)


if __name__ == "__main__":
    run()
