require('dotenv').config();
const { Pool } = require('pg');
const logger = require('./logger.js');
const statsCache = require('./cache.js'); // Importing cache

const pool = new Pool({
    connectionString: process.env.DATABASE_URL || 'postgresql://postgres:chicagobulls1@localhost:5432/tft_stats',
    ssl: process.env.DATABASE_URL ? true : false
});

const calculateAndInsertStats = async () => {
    try {
        const client = await pool.connect();
        logger.info('Connected to the database for stat calculations');

        // Check if stats are already in cache
        const cachedStats = statsCache.get("stats");
        if (cachedStats) {
            logger.info('Statistics retrieved from cache.');
            client.release();
            return cachedStats;
        }

        logger.info('Calculating and inserting statistics...');

        // Calculate and Insert Average Placement for each Augment
        let res = await client.query(`
            INSERT INTO tft_schema.augment_average_placement (augment_id, average_placement)
            SELECT augments.augment_id, AVG(matches.placement) AS avg_placement
            FROM tft_schema.augments
            JOIN tft_schema.match_augments ON augments.augment_id = match_augments.augment_id
            JOIN tft_schema.matches ON match_augments.match_id = matches.match_id
            GROUP BY augments.augment_id
            ON CONFLICT (augment_id) DO UPDATE 
            SET average_placement = EXCLUDED.average_placement;
        `);
        const averagePlacementUpdated = res.rowCount > 0;

        // Calculate and Insert Phase-Specific Placement Averages for each Augment
        res = await client.query(`
            INSERT INTO tft_schema.augment_phase_placement (augment_id, phase, average_placement)
            SELECT augments.augment_id, match_augments.phase, AVG(matches.placement) AS avg_placement
            FROM tft_schema.augments
            JOIN tft_schema.match_augments ON augments.augment_id = match_augments.augment_id
            JOIN tft_schema.matches ON match_augments.match_id = matches.match_id
            GROUP BY augments.augment_id, match_augments.phase
            ON CONFLICT (augment_id, phase) DO UPDATE 
            SET average_placement = EXCLUDED.average_placement;
        `);
        const phasePlacementUpdated = res.rowCount > 0;

        // Caching the status of operations
        const stats = {
            averagePlacementUpdated,
            phasePlacementUpdated
        };

        statsCache.set("stats", stats);
        logger.info('Statistics cached.');

        client.release();
        logger.info('Stat calculation and insertion process completed.');
    } catch (err) {
        logger.error(`Error in stat calculation and insertion: ${err}`);
    }
};

calculateAndInsertStats();
