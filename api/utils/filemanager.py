import csv
import logging

from api.track.schema import TrackSchema

track_schema = TrackSchema()


def validate_row(row):
    if len(row) == 3:
        origin, destination, cost = row
        track = {
            "origin": origin,
            "destination": destination,
            "cost": cost
        }
        error = track_schema.validate(track)
        if not error:
            return True
    return False


class FileManager:
    def __init__(self, file=None):
        self.file = file
        self.valid_rows = self.get_valid_rows()

    def is_file_valid(self):

        try:
            extension = self.file.split('.')[1]
            if not extension or extension != 'csv':
                raise IOError
            with open(self.file, "r") as read_file:
                if len(read_file.read()) == 0:
                    raise IOError
            return True
        except IOError:
            logging.error("\nInvalid file, please enter a CSV")
        return False

    def get_valid_rows(self):
        valid_rows = []
        try:
            if self.is_file_valid():
                with open(self.file, "r") as valid_csv:
                    csv_rows = csv.reader(valid_csv)
                    for row in csv_rows:
                        row[2] = float(row[2])
                        if not validate_row(row):
                            continue
                        valid_rows.append(row)
                valid_csv.close()
                return valid_rows
        except Exception:
            logging.error(f"Failed to get valid lines")
        return False

    def insert_new_line(self, track):
        try:
            with open(self.file, 'a+', newline='\n') as write_file:
                sheet_writer = csv.writer(
                    write_file,
                    delimiter=',',
                    quoting=csv.QUOTE_MINIMAL
                )
                sheet_writer.writerow(
                    [
                        track['origin'].upper(),
                        track['destination'].upper(),
                        float(track['cost'])
                    ]
                )
            write_file.close()
            self.valid_rows = self.get_valid_rows()
            return True
        except Exception as e:
            logging.error(f"Failed to save row")
            return e