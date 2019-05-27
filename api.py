import json
from db import *

from bottle import get, post, request, run, response, abort


@post('/playlist-delete/<playlist_id:int>/video/<video_id:int>/')
def delete_video_from_playlist(playlist_id, video_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    playlist_video = get_playlist_video(cursor, playlist_id, video_id)

    delete_and_arrange_positions(cursor, db, playlist_video["position"], playlist_video["id"], playlist_id, video_id)
    db.close()

    return json.dumps({"Status": "Video removed successfully"}, sort_keys=True)


@post('/playlist-add/<playlist_id:int>/video/<video_id:int>/')
def add_video_to_playlist(playlist_id, video_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    get_playlist(cursor, playlist_id)
    get_video(cursor, video_id)

    video_position = calculate_max_position(cursor, playlist_id)
    playlist_video = insert_video_in_playlist(cursor, db, playlist_id, video_id, video_position)

    db.close()
    response.headers['Content-Type'] = 'application/json'

    if not playlist_video:
        return json.dumps({"Status": "Something went wrong"}, sort_keys=True)
    return json.dumps({"Status": "Videos added successfully"}, sort_keys=True)


@post('/playlist-update/<playlist_id:int>/')
def playlist_update(playlist_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    playlist = get_playlist(cursor, playlist_id)

    name = request.forms.get('name')

    if not name:
        abort(403, "No data to update provided")

    cursor.execute("UPDATE playlists SET name=%s where id=%s;", (name, playlist_id,))
    db.commit()

    # Reselect updated record from database. With an object-like approach this could be avoided
    playlist = get_playlist(cursor, playlist_id)

    db.close()

    response.headers['Content-Type'] = 'application/json'
    return json.dumps(playlist, sort_keys=True)


@post('/playlist-delete/<playlist_id:int>/')
def playlist_delete(playlist_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM playlists where id=%s;", (playlist_id,))
    result = cursor.fetchone()

    if not result:
        abort(404, "Playlist Not Found")

    cursor.execute("DELETE FROM playlists where id=%s;", (result["id"],))

    db.commit()
    db.close()

    result["deleted"] = True

    response.headers['Content-Type'] = 'application/json'
    return json.dumps(result, sort_keys=True)


@post('/playlist-create/')
def playlist_create():
    name = request.forms.get('name')

    if not name:
        abort(403, "A Name must be provided")

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("INSERT INTO playlists (name) VALUES (%s);", (name, ))
    db.commit()

    created_id = cursor.lastrowid

    db.close()
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({"id": created_id}, sort_keys=True)


@get('/videos-list/')
def videos_list():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    videos = {"data": get_videos(cursor)}

    db.close()
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(videos, sort_keys=True)


@get('/playlists-list/')
def playlists_list():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    playlists = {"data": get_playlists(cursor)}

    db.close()
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(playlists, sort_keys=True)


@get('/playlist/<playlist_id:int>/')
def playlist(playlist_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    playlist = get_playlist(cursor, playlist_id)

    db.close()

    response.headers['Content-Type'] = 'application/json'
    return json.dumps(playlist, sort_keys=True)


@get('/playlist/<playlist_id:int>/videos/')
def playlist_videos(playlist_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # No need to assign it to a variable. I only need the check.
    get_playlist(cursor, playlist_id)
    videos = get_playlist_videos(cursor, playlist_id)

    db.close()
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(videos, sort_keys=True)


if __name__ == "__main__":
    run(host='localhost', port=7777, debug=True)
