DROP DATABASE dailymotion;

CREATE DATABASE dailymotion CHARACTER SET utf8 COLLATE utf8_general_ci;
USE dailymotion;

CREATE TABLE videos (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  url VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE playlists (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE playlist_video (
    id INT NOT NULL AUTO_INCREMENT,
    position INT NOT NULL DEFAULT 0,
    video_id int NOT NULL,
    playlist_id int NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY video_fk(video_id) REFERENCES videos(id) ON DELETE CASCADE,
    FOREIGN KEY playlist_fk(playlist_id) REFERENCES playlists(id) ON DELETE CASCADE
);


INSERT INTO videos ( name, url ) VALUES ( 'Video-1', 'http://videos/video-1/' );
INSERT INTO videos ( name, url ) VALUES ( 'Video-2', 'http://videos/video-2/' );
INSERT INTO videos ( name, url ) VALUES ( 'Video-3', 'http://videos/video-3/' );
INSERT INTO videos ( name, url ) VALUES ( 'Video-4', 'http://videos/video-4/' );
INSERT INTO videos ( name, url ) VALUES ( 'Video-5', 'http://videos/video-5/' );
