//require('dotenv').config();
const path = require('path');// new

require('dotenv').config({ path: path.join(__dirname, '../../../.env') });

const { Pool } = require('pg');

const pool = new Pool({
    connectionString: process.env.DATABASE_URL /*|| 'postgresql://postgres:chicagobulls1@localhost:5432/tft_stats'*/,
    //ssl: process.env.DATABASE_URL ? true : false
    ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});

module.exports = pool;
