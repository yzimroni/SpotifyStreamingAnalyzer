import unittest
import json
from spotify_streaming_analyzer import SpotifyStreamingAnalyzer


class SpotifyStreamingAnalyzerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.samples = []
        with open("samples/StreamingHistory0.json", "r", encoding="utf-8") as f:
            self.samples.append(json.load(f))
        with open("samples/StreamingHistory4.json", "r", encoding="utf-8") as f:
            self.samples.append(json.load(f))

    def test_add_streaming_history(self):
        analyzer = SpotifyStreamingAnalyzer()
        self.assertEqual(0, len(analyzer.get_streaming_history()))
        analyzer.add_streaming_history(self.samples[0])
        self.assertEqual(10000, len(analyzer.get_streaming_history()))
        analyzer.add_streaming_history(self.samples[1])
        self.assertEqual(10485, len(analyzer.get_streaming_history()))

    def test_data_framne(self):
        # Sample 1 test
        analyzer = SpotifyStreamingAnalyzer()
        analyzer.add_streaming_history(self.samples[0])
        analyzer.generate_data_frame()
        self.assertEqual(10000, analyzer.get_data_frame().shape[0])

        # Sample 2 test
        analyzer = SpotifyStreamingAnalyzer()
        analyzer.add_streaming_history(self.samples[1])
        analyzer.generate_data_frame()
        self.assertEqual(485, analyzer.get_data_frame().shape[0])

    def test_filter_by_date(self):
        # Sample 1 test
        analyzer = SpotifyStreamingAnalyzer()
        analyzer.add_streaming_history(self.samples[0])
        analyzer.generate_data_frame()
        analyzer.filter_by_date("2020-03-03")
        self.assertEqual(5366, analyzer.get_data_frame().shape[0])

        analyzer.filter_by_date("2020-05-03")
        self.assertEqual(1304, analyzer.get_data_frame().shape[0])

        analyzer.filter_by_date("2020-07-03")
        self.assertEqual(0, analyzer.get_data_frame().shape[0])

        # Sample 2 test
        analyzer = SpotifyStreamingAnalyzer()
        analyzer.add_streaming_history(self.samples[1])
        analyzer.generate_data_frame()
        analyzer.filter_by_date("2020-03-03")
        self.assertEqual(485, analyzer.get_data_frame().shape[0])

        analyzer.filter_by_date("2020-05-03")
        self.assertEqual(485, analyzer.get_data_frame().shape[0])

        analyzer.filter_by_date("2021-07-03")
        self.assertEqual(0, analyzer.get_data_frame().shape[0])

    def test_analyze(self):
        # Sample 1 test
        analyzer = SpotifyStreamingAnalyzer()
        analyzer.add_streaming_history(self.samples[0])
        analyzer.generate_data_frame()
        analyzer.analyze()
        r = analyzer.get_result()
        self.assertEqual({'Count': 6, 'TotalSecPlayed': 383, 'AvgSecPerPlay': 63, 'FirstPlayed': '2019-12-29 20:19', 'LastPlayed': '2020-04-19 17:14'}, r.iloc[4].to_dict())
        self.assertEqual({'Count': 5, 'TotalSecPlayed': 175, 'AvgSecPerPlay': 35, 'FirstPlayed': '2019-12-29 20:12', 'LastPlayed': '2020-04-13 15:55'}, r.iloc[25].to_dict())
        self.assertEqual({'Count': 22, 'TotalSecPlayed': 2690, 'AvgSecPerPlay': 122, 'FirstPlayed': '2020-02-06 18:19', 'LastPlayed': '2020-05-22 19:36'}, r.iloc[100].to_dict())

        # Sample 2 test
        analyzer = SpotifyStreamingAnalyzer()
        analyzer.add_streaming_history(self.samples[1])
        analyzer.generate_data_frame()
        analyzer.analyze()
        r = analyzer.get_result()
        self.assertEqual({'Count': 1, 'TotalSecPlayed': 285, 'AvgSecPerPlay': 285, 'FirstPlayed': '2020-12-21 12:41', 'LastPlayed': '2020-12-21 12:41'}, r.iloc[5].to_dict())
        self.assertEqual({'Count': 1, 'TotalSecPlayed': 2, 'AvgSecPerPlay': 2, 'FirstPlayed': '2020-12-22 06:01', 'LastPlayed': '2020-12-22 06:01'}, r.iloc[25].to_dict())
        self.assertEqual({'Count': 1, 'TotalSecPlayed': 172, 'AvgSecPerPlay': 172, 'FirstPlayed': '2020-12-22 08:57', 'LastPlayed': '2020-12-22 08:57'}, r.iloc[30].to_dict())

    def test_filter_by_play_count(self):
        # Sample 1 test
        analyzer = SpotifyStreamingAnalyzer()
        analyzer.add_streaming_history(self.samples[0])
        analyzer.generate_data_frame()
        analyzer.analyze()
        analyzer.filter_by_play_count(10)
        self.assertEqual(368, analyzer.get_result().shape[0])

        analyzer.filter_by_play_count(12)
        self.assertEqual(312, analyzer.get_result().shape[0])

        analyzer.filter_by_play_count(22)
        self.assertEqual(108, analyzer.get_result().shape[0])

        analyzer.filter_by_play_count(200)
        self.assertEqual(0, analyzer.get_result().shape[0])

        # Sample 2 test
        analyzer = SpotifyStreamingAnalyzer()
        analyzer.add_streaming_history(self.samples[1])
        analyzer.generate_data_frame()
        analyzer.analyze()
        analyzer.filter_by_play_count(2)
        self.assertEqual(81, analyzer.get_result().shape[0])

        analyzer.filter_by_play_count(3)
        self.assertEqual(24, analyzer.get_result().shape[0])

        analyzer.filter_by_play_count(4)
        self.assertEqual(4, analyzer.get_result().shape[0])

        analyzer.filter_by_play_count(10)
        self.assertEqual(0, analyzer.get_result().shape[0])


if __name__ == '__main__':
    unittest.main()
