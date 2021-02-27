import unittest
import utils


class UtilsTest(unittest.TestCase):
    def test_get_streaming_history_files(self):
        self.assertEqual([], utils.get_streaming_history_files("."))
        self.assertEqual(['StreamingHistory0.json', 'StreamingHistory4.json'], utils.get_streaming_history_files("samples"))


if __name__ == '__main__':
    unittest.main()
