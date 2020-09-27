DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS news;
DROP TABLE IF EXISTS track;
DROP TABLE IF EXISTS food_track;
DROP TABLE IF EXISTS symptom_track;

CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	email TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL,
	access_token TEXT NOT NULL,
  color TEXT,
  verification_token TEXT,
	verified INTEGER DEFAULT 0
);

CREATE TABLE news (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	source TEXT,
	author TEXT,
	title TEXT NOT NULL,
	description TEXT,
	url TEXT NOT NULL,
	image TEXT,
	publish_date TEXT NOT NULL
);

CREATE TABLE track (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER,
  water_count INTEGER,
	date TEXT NOT NULL
);

CREATE TABLE food_track (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
  track_id INTEGER,
  name TEXT,
  description TEXT
);

CREATE TABLE symptom_track (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
  track_id INTEGER,
  symptom INTEGER,
  body_parts TEXT,
  intensity INTEGER
);
