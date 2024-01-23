require('dotenv').config();
const { Pool } = require('pg');
const logger = require('./logger.js');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://postgres:chicagobulls1@localhost:5432/tft_stats',
  ssl: process.env.DATABASE_URL ? true : false
});

// Function to check if recalculation is needed
const shouldRecalculate = async (client) => {
  const res = await client.query(`
    SELECT MAX(last_updated) as last_updated
    FROM (
      SELECT last_updated FROM tft_schema.augment_average_placement
      UNION ALL
      SELECT last_updated FROM tft_schema.augment_phase_placement
    ) as combined
  `);

  const lastUpdated = res.rows[0].last_updated;
  const twoHoursAgo = new Date(Date.now() - 2 * 60 * 60 * 1000);

  return !lastUpdated || lastUpdated < twoHoursAgo;
};

const calculateAndInsertStats = async () => {
  try {
    const client = await pool.connect();
    logger.info('Connected to the database for stat calculations');

    if (!(await shouldRecalculate(client))) {
      logger.info('Statistics are up-to-date. No need to recalculate.');
      client.release();
      return;
    }

    logger.info('Calculating and inserting statistics...');

    // Calculate and Insert Average Placement for each Augment
    let res = await client.query(`
      INSERT INTO tft_schema.augment_average_placement (augment_id, average_placement, last_updated)
      SELECT augments.augment_id, AVG(matches.placement) AS avg_placement, CURRENT_TIMESTAMP
      FROM tft_schema.augments
      JOIN tft_schema.match_augments ON augments.augment_id = match_augments.augment_id
      JOIN tft_schema.matches ON match_augments.match_id = matches.match_id
      GROUP BY augments.augment_id
      ON CONFLICT (augment_id) DO UPDATE 
      SET average_placement = EXCLUDED.average_placement, last_updated = CURRENT_TIMESTAMP;
    `);
    logger.info('Average placement statistics updated.');

    // Calculate and Insert Phase-Specific Placement Averages for each Augment
    /*res = await client.query(`
      INSERT INTO tft_schema.augment_phase_placement (augment_id, phase, average_placement, last_updated)
      SELECT augments.augment_id, match_augments.phase, AVG(matches.placement) AS avg_placement, CURRENT_TIMESTAMP
      FROM tft_schema.augments
      JOIN tft_schema.match_augments ON augments.augment_id = match_augments.augment_id
      JOIN tft_schema.matches ON match_augments.match_id = matches.match_id
      GROUP BY augments.augment_id, match_augments.phase
      ON CONFLICT (id) DO UPDATE 
      SET average_placement = EXCLUDED.average_placement, last_updated = CURRENT_TIMESTAMP;
    `);
    logger.info('Phase-specific placement statistics updated.');*/

    // Calculate and Insert Phase-Specific Placement Averages for each Augment
    res = await client.query(`
      INSERT INTO tft_schema.augment_phase_placement (augment_id, phase, average_placement, last_updated)
      SELECT augments.augment_id, match_augments.phase, AVG(matches.placement) AS avg_placement, CURRENT_TIMESTAMP
      FROM tft_schema.augments
      JOIN tft_schema.match_augments ON augments.augment_id = match_augments.augment_id
      JOIN tft_schema.matches ON match_augments.match_id = matches.match_id
      GROUP BY augments.augment_id, match_augments.phase
      ON CONFLICT (augment_id, phase) DO UPDATE 
      SET average_placement = EXCLUDED.average_placement, last_updated = CURRENT_TIMESTAMP;
    `);
    logger.info('Phase-specific placement statistics updated.');

    client.release();
    logger.info('Stat calculation and insertion process completed.');
  } catch (err) {
    logger.error(`Error in stat calculation and insertion: ${err}`);
    if (client) {
      client.release();
    }
  }
};

calculateAndInsertStats();
