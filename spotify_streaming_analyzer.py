class SpotifyStreamingAnalyzer:

    def __init__(self):
        self.streaming = []

    def add_streaming_history(self, history):
        """
        Add streaming history records to the streaming list
        :param history: A list of streaming records
        """
        self.streaming.extend(history)
