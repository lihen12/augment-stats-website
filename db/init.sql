CREATE SCHEMA tft_schema;

-- Players Table
CREATE TABLE tft_schema.players (
    player_id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- Augments Table
CREATE TABLE tft_schema.augments (
    augment_id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    times_played INT DEFAULT 0
);

-- Matches Table
CREATE TABLE tft_schema.matches (
    match_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES tft_schema.players(player_id),
    placement INT NOT NULL,
    unique_id TEXT UNIQUE
);

-- MatchAugments Table
CREATE TABLE tft_schema.match_augments (
    match_augment_id SERIAL PRIMARY KEY,
    match_id INT REFERENCES tft_schema.matches(match_id),
    augment_id INT REFERENCES tft_schema.augments(augment_id),
    phase TEXT NOT NULL,
    placement INT NOT NULL
);
