DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS news;

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
