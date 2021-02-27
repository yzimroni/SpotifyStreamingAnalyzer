import pandas as pd


class SpotifyStreamingAnalyzer:

    def __init__(self):
        self.streaming = []

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

    def analyze(self):
        """
        Analyze streaming history
        :return: DataFrame of the analyzed data
        """
        # Create pandas DataFrame from streaming list
        df = pd.DataFrame(self.streaming)
        # Group by tracks (identified by artist and track names)
        gr = df.groupby(["artistName", "trackName"])
        # Aggregate results
        # Values are deviced by 1000 to convert ms to seconds
        gr = gr.agg({"msPlayed": ["count", lambda x: int(x.sum() / 1000), lambda x: int((x.sum() / x.count()) / 1000)],
                     "endTime": ["min", "max"]})
        # Rename colums
        gr.columns = ["Count", "TotalSecPlayed", "AvgSecPerPlay", "FirstPlayed", "LastPlayed"]
        return gr
