def list_tracks(valid_tracks):
    tracks = []
    for row in valid_tracks:
        single_track = {
            "origin": row[0],
            "destination": row[1],
            "cost": row[2]
        }
        tracks.append(single_track)
    return tracks


def check_input_exists(valid_tracks, track_input):
    track_options = []
    for track in valid_tracks:
        track_options.append(track[0])
        track_options.append(track[1])
    track_options = list(dict.fromkeys(track_options))
    return track_input['origin'] in track_options and track_input['destination'] in track_options

