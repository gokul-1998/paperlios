-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  college_reg_no TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email TEXT NOT NULL
);
CREATE TABLE faculty (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  college_reg_no TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email TEXT NOT NULL
);

CREATE TABLE proposal (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  to_email TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  event_description TEXT NOT NULL,
  status TEXT DEFAULT false,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (to_email) REFERENCES faculty (email)
);

CREATE TABLE dutyleave (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  to_email TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  duty_leave_description TEXT NOT NULL,
  status TEXT DEFAULT false,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (to_email) REFERENCES faculty (email)
);
