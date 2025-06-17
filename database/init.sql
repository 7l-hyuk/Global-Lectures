CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(256) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE video (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    length VARCHAR(16) NOT NULL,
    key TEXT,                           -- videos/${video_id}.mp4    e.g., videos/1.mp4
    voice_id VARCHAR(32),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    creator_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    description TEXT
);

CREATE TABLE video_language (
    video_id INTEGER NOT NULL REFERENCES video(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,     -- e.g., 'en', 'ko'
    audio_key TEXT,                     -- audios/${video_id}/${lang_code}.wav       e.g., audios/1/ko.wav
    subtitle_key TEXT,                  -- subtitles/${video_id}/${lang_code}.json    e.g., subtitles/1/ko.json
    PRIMARY KEY (video_id, lang_code)
);