import json
from http.client import BAD_REQUEST, CREATED, NOT_FOUND

from flask.views import MethodView
from flask import request, Response

from api.track.exceptions import CustomException
from api.track.schema import TrackSchema
from api.track.helpers import list_tracks, check_input_exists
from api.utils.dijkstra import Dijkstra
track_schema = TrackSchema()


class TrackView(MethodView):
    def get(self, file_manager):
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        track_input = {
            "origin": origin,
            "destination": destination
        }
        if origin or destination:
            error = track_schema.validate(track_input)
            if error:
                raise CustomException(error, BAD_REQUEST)
            if track_input:
                track_input['origin'] = track_input['origin'].upper()
                track_input['destination'] = track_input['destination'].upper()
                valid_tracks = file_manager.valid_rows
                if not check_input_exists(valid_tracks, track_input):
                    raise CustomException("Origin or Destination not found", NOT_FOUND)
                result = Dijkstra(valid_tracks, track_input['origin'], track_input['destination']).get_best_path()
                if result:
                    return result
                raise CustomException("Track doesn't exist", NOT_FOUND)
        return {
            "tracks": list_tracks(file_manager.valid_rows)
        }

    def post(self, file_manager):
        request_body = json.loads(request.data)
        error = track_schema.validate(request_body)
        if error:
            raise CustomException(error, BAD_REQUEST)
        row_saved = file_manager.insert_new_line(request_body)
        if row_saved is True:
            return Response(json.dumps(request_body), status=CREATED, mimetype='application/json')
        raise CustomException("Internal server error")



