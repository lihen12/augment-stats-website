require('dotenv').config();
const { Pool } = require('pg');

const pool = new Pool({
    connectionString: process.env.DATABASE_URL || 'postgresql://postgres:chicagobulls1@localhost:5432/tft_stats',
    ssl: process.env.DATABASE_URL ? true : false
})

const testConnection = async () => {
  try {
    console.log('Connecting to the database...');
    const client = await pool.connect();
    console.log('Successfully connected to the database');
    client.release();
    console.log('Connection released');
  } catch (err) {
    console.error('Error connecting to the database:', err);
  }
};

testConnection();
