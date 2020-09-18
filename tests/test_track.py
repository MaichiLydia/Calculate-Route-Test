import csv
import json
import unittest
from app import app
from api.settings.config import config_by_name
from api.track.helpers import list_tracks
from api.track.views import TrackView
from api.utils.filemanager import FileManager

csv_initial_values = [
    'GRU,BRC,10',
    'BRC,SCL,5',
    'GRU,CDG,75',
    'GRU,SCL,20',
    'GRU,ORL,56',
    'ORL,CDG,5',
    'SCL,ORL,20',
    'CDG,ORL,5'
]


def file_initial_values():
    with open('tests/input-file-test.csv', '+w', newline='\n') as write_file:
        sheet_writer = csv.writer(
            write_file,
            delimiter=',',
            quoting=csv.QUOTE_MINIMAL
        )
        for row in csv_initial_values:
            origin, destination, cost = row.split(',')
            sheet_writer.writerow(
                [
                    origin,
                    destination,
                    float(cost)
                ]
            )
    write_file.close()


class TestTrackCase(unittest.TestCase):
    def tearDown(self):
        file_initial_values()

    @classmethod
    def setUpClass(cls):
        environment = 'test'
        app.config.from_object(config_by_name[environment])
        cls.file = FileManager('tests/input-file-test.csv')
        app.add_url_rule("/v1/track", defaults={"file_manager": cls.file}, view_func=TrackView.as_view("trackview"))
        cls.client = app.test_client()

    def test_get_all_tracks_without_query_param(self):
        response = self.client.get('/v1/track')
        tracks = json.loads(response.data)['tracks']
        self.assertEqual(tracks, list_tracks(self.file.valid_rows))

    def test_get_best_path(self):
        response = self.client.get('/v1/track', query_string={"origin": 'GRU', "destination": "CDG"})
        json_response = json.loads(response.data)
        self.assertEqual(json_response["cost"], "R$ 40.0")
        self.assertEqual(json_response["path"], "GRU > BRC > SCL > ORL > CDG")

    def test_404_query_param(self):
        response = self.client.get('/v1/track', query_string={"origin": "GRU", "destination": "ABA"})
        json_response = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response["message"], "Origin or Destination not found")

    def test_post_new_route_and_404_route(self):
        response = self.client.post('/v1/track',
                                    data=json.dumps({"origin": "TES", "destination": "ABA", "cost": 15}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)
        response_get_path_not_tracked = self.client.get('/v1/track', query_string={"origin": "GRU", "destination": "TES"})
        json_response = json.loads(response_get_path_not_tracked.data)
        self.assertEqual(response_get_path_not_tracked.status_code, 404)
        self.assertEqual(json_response["message"], "Track doesn't exist")

    def test_post_invalid_origin(self):
        response = self.client.post('/v1/track',
                                    data=json.dumps({"origin": "bass", "destination": "ABA", "cost": 15}),
                                    content_type="application/json")
        json_response = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], {'origin': ['Length must be between 3 and 3.']})

    def test_post_invalid_destination(self):
        response = self.client.post('/v1/track',
                                    data=json.dumps({"origin": "EAD", "destination": "sd", "cost": 15}),
                                    content_type="application/json")
        json_response = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], {'destination': ['Length must be between 3 and 3.']})