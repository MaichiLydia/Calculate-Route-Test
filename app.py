import os
import sys
import logging
from flask import Flask, jsonify
from api.track.exceptions import CustomException
from api.track.views import TrackView
from api.settings.config import config_by_name
from api.utils.filemanager import FileManager
app = Flask(__name__)


@app.errorhandler(CustomException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    system_inputs = sys.argv
    if len(system_inputs) < 2:
        logging.error(f"""
Please enter a file and a optional environment setting('dev', 'test', 'prod')
Example: python app.py file.csv dev
            or
         python app.py file.csv
        """)
    else:
        filename = system_inputs[1]
        environment = system_inputs[2] if len(system_inputs) >= 3 else os.getenv('ENV') or 'dev'
        app.config.from_object(config_by_name[environment])
        file = FileManager(filename)
        if file.is_file_valid():
            app.add_url_rule("/v1/track", defaults={"file_manager": file}, view_func=TrackView.as_view("trackview"))
            app.run(host='127.0.0.1', port='8080')

