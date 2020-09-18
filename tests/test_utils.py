import csv
import unittest

from api.utils.dijkstra import Dijkstra
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


class FileManagerTestCase(unittest.TestCase):
    def tearDown(self):
        file_initial_values()

    @classmethod
    def setUpClass(cls):
        cls.invalid_path = 'tests/input-file-test.txt'
        cls.valid_path = 'tests/input-file-test.csv'

    def test_invalid_path(self):
        file = FileManager(self.invalid_path)
        assert not file.is_file_valid()

    def test_valid_path(self):
        file = FileManager(self.valid_path)
        self.assertEqual(file.valid_rows, [
            ['GRU', 'BRC', 10.0],
            ['BRC', 'SCL', 5.0],
            ['GRU', 'CDG', 75.0],
            ['GRU', 'SCL', 20.0],
            ['GRU', 'ORL', 56.0],
            ['ORL', 'CDG', 5.0],
            ['SCL', 'ORL', 20.0],
            ['CDG', 'ORL', 5.0]
        ])
        assert file.is_file_valid()

    def test_insert_line(self):
        file = FileManager(self.valid_path)
        track = {
            "origin": "EPA",
            "destination": "ACE",
            "cost": 25
        }
        did_saved = file.insert_new_line(track)
        assert file.is_file_valid()
        assert did_saved


class DijkstraTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid_rows = [
            ['GRU', 'BRC', 10.0],
            ['BRC', 'SCL', 5.0],
            ['GRU', 'CDG', 75.0],
            ['GRU', 'SCL', 20.0],
            ['GRU', 'ORL', 56.0],
            ['ORL', 'CDG', 5.0],
            ['SCL', 'ORL', 20.0],
            ['CDG', 'ORL', 5.0],
            ['BAT', 'AES', 10.0]
        ]

    def test_get_graph(self):
        dijkstra = Dijkstra(self.valid_rows, 'GRU', 'CDG')
        expected_graph = {
            'GRU': {'BRC': 10.0, 'CDG': 75.0, 'SCL': 20.0, 'ORL': 56.0},
            'BRC': {'SCL': 5.0},
            'SCL': {'ORL': 20.0},
            'CDG': {'ORL': 5.0},
            'ORL': {'CDG': 5.0},
            'BAT': {'AES': 10.0},
            'AES': {}
        }
        self.assertEqual(dijkstra.graph, expected_graph)

    def test_get_best_path(self):
        dijkstra = Dijkstra(self.valid_rows, 'GRU', 'CDG')
        self.assertEqual(dijkstra.get_best_path(), {'cost': 'R$ 40.0', 'path': 'GRU > BRC > SCL > ORL > CDG'})

    def test_path_not_accessible(self):
        dijkstra = Dijkstra(self.valid_rows, 'GRU', 'AES')
        assert not dijkstra.get_best_path()