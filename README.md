# dailymotion_test


# Build the container

sudo docker build --tag=dailymotiontest .

sudo docker run --net=host -p 7777 dailymotiontest

I've used the --net=host option because I wanted to use my already installed ( locally ) mysql database.

You can connect to the container with http://localhost:7777/.

Some of the endpoints below are accessible via GET requests. The dispositive ones via POST.

You can use curl or any other client to interact with these basic APIs.


# Test API endpoints.

/playlist-delete/<playlist_id:int>/video/<video_id:int>/

/playlist-add/<playlist_id:int>/video/<video_id:int>/

/playlist-update/<playlist_id:int>/

/playlist-delete/<playlist_id:int>/

/playlist-create/

/videos-list/

/playlists-list/

/playlist/<playlist_id:int>/

/playlist/<playlist_id:int>/videos/



