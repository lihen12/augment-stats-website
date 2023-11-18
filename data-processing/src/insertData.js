require('dotenv').config();
const { Pool } = require('pg');
const fs = require('fs');
const path = require('path');
const logger = require('./logger.js');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://postgres:chicagobulls1@localhost:5432/tft_stats',
  ssl: process.env.DATABASE_URL ? true : false
});

const insertData = async () => {
  try {
    const client = await pool.connect();
    logger.info('Connected to the database');

    const files = fs.readdirSync(path.join(__dirname, '../../data/json'));
    for (const file of files) {
      if (file.endsWith('.json')) {
        const data = JSON.parse(fs.readFileSync(path.join(__dirname, '../../data/json', file), 'utf8'));
        logger.info(`Processing file: ${file}`);

        const playerName = file.replace(/_matches_data\.json$/, '').replace(/_/g, ' ');
        let res = await client.query('INSERT INTO tft_schema.players (name) VALUES ($1) ON CONFLICT (name) DO NOTHING RETURNING player_id', [playerName]);
        let playerId = res.rows[0]?.player_id;

        if (!playerId) {
          res = await client.query('SELECT player_id FROM tft_schema.players WHERE name = $1', [playerName]);
          playerId = res.rows[0].player_id;
        }

        for (const match of data) {
          // Check if a match with the unique_id already exists
          const uniqueId = match.unique_id;
          res = await client.query('SELECT match_id FROM tft_schema.matches WHERE unique_id = $1', [uniqueId]);
          if (res.rows.length === 0) {
            // Insert the match if it doesn't exist
            res = await client.query('INSERT INTO tft_schema.matches (player_id, placement, unique_id) VALUES ($1, $2, $3) RETURNING match_id', [playerId, match.placement, uniqueId]);
            const matchId = res.rows[0].match_id;

            for (const phase in match.augments) {
              const augmentName = match.augments[phase];
              if (augmentName) {
                let augmentId;
                res = await client.query('INSERT INTO tft_schema.augments (name) VALUES ($1) ON CONFLICT (name) DO NOTHING RETURNING augment_id', [augmentName]);
                augmentId = res.rows[0]?.augment_id;

                if (!augmentId) {
                  res = await client.query('SELECT augment_id FROM tft_schema.augments WHERE name = $1', [augmentName]);
                  augmentId = res.rows[0].augment_id;
                }

                await client.query('INSERT INTO tft_schema.match_augments (match_id, augment_id, phase, placement) VALUES ($1, $2, $3, $4)', [matchId, augmentId, phase, match.placement]);
                logger.info(`Inserted augment: ${augmentName} for match ID: ${matchId}`);
              }
            }
          } else {
            logger.info(`Match with unique ID ${uniqueId} already exists, skipping insertion.`);
          }
        }
      }
    }

    client.release();
    logger.info('Data insertion complete');
  } catch (err) {
    logger.error(`Error in data insertion: ${err}`);
  }
};

insertData();

