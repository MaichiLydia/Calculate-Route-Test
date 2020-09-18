import csv
import unittest
from unittest import mock

import console
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
        file_path = 'tests/input-file-test.csv'
        cls.argv = ['app', file_path]
        cls.file = FileManager(file_path)

    @mock.patch('logging.error')
    def test_main_without_file(
            self,
            mock_logging
    ):
        console.main([])
        mock_logging.assert_called_once()

    @mock.patch('console.handle_choice', return_result=True)
    @mock.patch('builtins.input', side_effect=[1, "a"])
    @mock.patch('logging.error')
    def test_main_exit(
            self,
            mock_logging,
            mock_input,
            mock_handle_choice
    ):
        result = console.main(self.argv)
        mock_logging.assert_not_called()
        mock_handle_choice.assert_called()
        self.assertEqual(result, 0)

    @mock.patch('builtins.input', side_effect=["GRU", "CDG"])
    def test_get_best_path(
            self,
            mock_input_destination
    ):
        response = console.handle_choice(1, self.file)
        self.assertTrue(response)

    @mock.patch('builtins.input', side_effect=["GRU", "AES", "a"])
    def test_fail_get_best_path(
            self,
            mock_input_destination
    ):
        response = console.handle_choice(1, self.file)
        self.assertFalse(response)

    @mock.patch('builtins.input', side_effect=["GRU", "AED", 30])
    def test_save_track(
            self,
            mock_input_destination
    ):
        response = console.handle_choice(2, self.file)
        self.assertTrue(response)

    def test_valid_track(self):
        origin = 'GRU'
        destination = 'EAD'
        body = console.get_valid_input(origin, destination)
        self.assertEqual(body, {
            "origin": origin,
            "destination": destination
        })

    def test_invalid_track(self):
        origin = 'GRU'
        destination = 'EADs'
        body = console.get_valid_input(origin, destination)
        self.assertFalse(body)