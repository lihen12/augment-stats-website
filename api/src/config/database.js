require('dotenv').config();

const { Pool } = require('pg');

const pool = new Pool({
    connectionString: process.env.DATABASE_URL || 'postgresql://postgres:chicagobulls1@localhost:5432/tft_stats',
    ssl: process.env.DATABASE_URL ? true : false
});

module.exports = pool;
