import pandas as pd


class SpotifyStreamingAnalyzer:

    def __init__(self):
        self.streaming = []
        self.data_frame = None
        self.grouped_data = None

    def add_streaming_history(self, history):
        """
        Add streaming history records to the streaming list
        :param history: A list of streaming records
        """
        self.streaming.extend(history)

    def get_streaming_history(self):
        """
        Get the streaming history list
        :return: Current streaming history list
        """
        return self.streaming

    def get_data_frame(self):
        """
        Get the dataframe used for analyzing
        :return: Current dataframe
        """
        return self.data_frame

    def generate_data_frame(self):
        """
        Generate DataFrame from streaming history
        """
        self.data_frame = pd.DataFrame(self.streaming)

    def filter_by_date(self, from_date):
        """
        Filter streaming history before a specific date
        :param from_date: The date to filter from (fromat: YYYY-MM-DD)
        """
        filtered = self.data_frame[self.data_frame["endTime"] > from_date]
        self.data_frame = filtered

    def analyze(self):
        """
        Analyze streaming history
        """
        # Create pandas DataFrame from streaming list
        # Group by tracks (identified by artist and track names)
        self.grouped_data = self.data_frame.groupby(["artistName", "trackName"])
        # Aggregate results
        # Values are divided by 1000 to convert ms to seconds
        self.grouped_data = self.grouped_data.agg(
            {"msPlayed": ["count", lambda x: int(x.sum() / 1000), lambda x: int((x.sum() / x.count()) / 1000)],
             "endTime": ["min", "max"]})
        # Rename columns
        self.grouped_data.columns = ["Count", "TotalSecPlayed", "AvgSecPerPlay", "FirstPlayed", "LastPlayed"]

    def filter_by_play_count(self, count):
        """
        Filter songs below a specific play count.
        :param count: Minimum song play count
        """
        filtered = self.grouped_data[self.grouped_data["Count"] >= count]
        self.grouped_data = filtered

    def get_result(self):
        """
        Get the analyzed data
        :return: DataFrame of the analyzed data
        """
        return self.grouped_data
