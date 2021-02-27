# Spotify Streaming Analyzer
Analyze your Spotify's streaming history

This tool will analyze your Spotify streaming history and will generate a file containing aggregated data about your streaming history

# Usage
To use the tool you need to export your data from Spotify, which can be done [here](https://www.spotify.com/us/account/privacy/) (under "Download your data").

It might take a few days before you can download your data.

Once you downloaded your data, extract the zip and run the program:
```
python analyze.py --source <path to your extracted zip/MyData> --output <output_file.csv>
```

For example:
```
python analyze.py --source Downloads/my_spotify_data/MyData --output output.csv
```

You can use filters to filter streaming history before a specific date, using the --from-date flag, and filter songs below a specific play count, using --min-count
```
python analyze.py --source Downloads/my_spotify_data/MyData --output output.csv --from-date 2019-03-04 --min-count 5
```
