import unittest
from api.track.helpers import list_tracks, check_input_exists


class HelpersTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid_rows = [
            ['GRU', 'BRC', 10.0],
            ['BRC', 'SCL', 5.0]
        ]

    def test_list_tracks(self):
        tracks_list = list_tracks(self.valid_rows)
        expected_payload = [{'origin': 'GRU', 'destination': 'BRC', 'cost': 10.0}, {'origin': 'BRC', 'destination': 'SCL', 'cost': 5.0}]
        self.assertEqual(tracks_list, expected_payload)

    def test_check_input_exists_true(self):
        track_input = {
            "origin": "GRU",
            "destination": "SCL"
        }
        track_exists = check_input_exists(self.valid_rows, track_input)
        self.assertTrue(track_exists)

    def test_check_input_exists_false(self):
        track_input = {
            "origin": "ABA",
            "destination": "SCL"
        }
        track_exists = check_input_exists(self.valid_rows, track_input)
        self.assertFalse(track_exists)