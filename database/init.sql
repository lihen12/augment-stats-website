-- Players Table
CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

-- Augments Table
CREATE TABLE augments (
    augment_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    times_played INT DEFAULT 0
);

-- Matches Table
CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id),
    placement INT NOT NULL
);

-- MatchAugments Table
CREATE TABLE match_augments (
    match_augment_id SERIAL PRIMARY KEY,
    match_id INT REFERENCES matches(match_id),
    augment_id INT REFERENCES augments(augment_id),
    phase TEXT NOT NULL,
    placement INT NOT NULL
);
