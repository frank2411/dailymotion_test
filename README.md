# dailymotion_test


# Build the container

sudo docker build --tag=dailymotiontest .

sudo docker run --net=host -p 7777 dailymotiontest

I've used the --net=host option because I wanted to use my already installed ( locally ) mysql database.

You can connect to the container with http://localhost:7777/.

Some of the endpoints below are accessible via GET requests. The dispositive ones via POST.

You can use curl or any other client to interact with these basic APIs.

# Import the db.sql file in mysql

This file creates some videos entities and creates all the tables needed.

mysql -u <users> -p < db.sql


# Test API endpoints.

/playlist-delete/<playlist_id:int>/video/<video_id:int>/  POST -> to delete a video inside a playlist

/playlist-add/<playlist_id:int>/video/<video_id:int>/ POST -> to add a video inside a playlist

/playlist-update/<playlist_id:int>/ POST -> this can update the playlist name

/playlist-delete/<playlist_id:int>/ POST -> this deletes the target playlist

/playlist-create/ POST -> creates a playlist with a name attribute

/videos-list/ GET -> list of all videos

/playlists-list/ GET -> list of all playlists

/playlist/<playlist_id:int>/ GET -> display some playlist infos 

/playlist/<playlist_id:int>/videos/ GET ->lists all playlist videos ordered by position

# Conclusion

I've concetrated myself more on the functionality aspects than making complex model with lot of infos.
So The video and playlist Models have the fields that you suggested but, on the other end, all the functionality are fully implemented.





