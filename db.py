import mysql.connector
from mysql.connector import errorcode
from bottle import abort


def get_db_connection():

    try:
        connection = mysql.connector.connect(
            user='root',
            password='admin',
            host='127.0.0.1',
            database='dailymotion'
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

        return

    return connection


def get_playlists(cursor):
    cursor.execute("SELECT * FROM playlists;")
    results = cursor.fetchall()
    return results


def get_playlist(cursor, playlist_id):
    cursor.execute("SELECT * FROM playlists where id=%s;", (playlist_id,))
    result = cursor.fetchone()

    if not result:
        abort(404, "Playlist Not Found")

    return result


def get_playlist_videos(cursor, playlist_id):
    cursor.execute(
        """
            SELECT videos.*
            FROM videos
            INNER JOIN playlist_video ON playlist_video.playlist_id = %s
            WHERE playlist_video.video_id = videos.id order by playlist_video.position;
        """, (playlist_id,))

    videos = cursor.fetchall()
    return videos


def get_playlist_video(cursor, playlist_id, video_id):
    cursor.execute(
        "SELECT * FROM playlist_video where playlist_id=%s AND video_id=%s;", (playlist_id, video_id)
    )

    result = cursor.fetchone()

    if not result:
        abort(404, "Video in Playlist Not Found")

    return result


def get_videos(cursor):
    cursor.execute("SELECT * FROM videos;")
    results = cursor.fetchall()
    return results


def get_video(cursor, video_id):
    cursor.execute("SELECT * FROM videos where id=%s;", (video_id,))
    result = cursor.fetchone()

    if not result:
        abort(404, "Video Not Found")

    return result


def calculate_max_position(cursor, playlist_id):
    cursor.execute("SELECT max(position) as position FROM playlist_video where playlist_id=%s;", (playlist_id,))
    result = cursor.fetchone()

    position = 1
    if result["position"] is not None:
        position = result["position"] + 1
    return position


def insert_video_in_playlist(cursor, db, playlist_id, video_id, position):
    cursor.execute("""
        INSERT INTO playlist_video(position, video_id, playlist_id) VALUES (%s, %s, %s);
        """, (position, video_id, playlist_id)
    )

    db.commit()
    return cursor.lastrowid


def delete_and_arrange_positions(cursor, db, current_position, playlist_video_id, playlist_id, video_id):
    cursor.execute("DELETE FROM playlist_video where id=%s;", (playlist_video_id,))

    cursor.execute(
        "SELECT * from playlist_video where position > %s AND playlist_id=%s;",
        (current_position, playlist_id)
    )

    results = cursor.fetchall()

    for res in results:
        cursor.execute(
            "UPDATE playlist_video SET position = (position - 1) WHERE id=%s;",
            (res["id"],)
        )

    db.commit()

    return True
