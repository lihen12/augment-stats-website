const express = require('express');
const pool = require('./config/database');
const cors = require('cors');

const app = express();
app.use(cors()); // Enable CORS for frontend integration
app.use(express.json()); // Middleware for parsing JSON

const port = process.env.PORT || 3000;

// Route to fetch data for the table
app.get('/api/augments/stats', async (req, res) => {
    try {
        const client = await pool.connect();
        const query = `
            SELECT 
                a.name, 
                a.times_played, 
                aa.average_placement, 
                ap2.average_placement AS placement_2_1, 
                ap3.average_placement AS placement_3_2, 
                ap4.average_placement AS placement_4_2
            FROM tft_schema.augments a
            LEFT JOIN tft_schema.augment_average_placement aa ON a.augment_id = aa.augment_id
            LEFT JOIN tft_schema.augment_phase_placement ap2 ON a.augment_id = ap2.augment_id AND ap2.phase = '2-1'
            LEFT JOIN tft_schema.augment_phase_placement ap3 ON a.augment_id = ap3.augment_id AND ap3.phase = '3-2'
            LEFT JOIN tft_schema.augment_phase_placement ap4 ON a.augment_id = ap4.augment_id AND ap4.phase = '4-2';
        `;
        const result = await client.query(query);
        res.json(result.rows);
        client.release();
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: err.message });
    }
});

// Search endpoint for augments
app.get('/api/augments/search', async (req, res) => {
    const searchTerm = req.query.term;
    if (!searchTerm) {
        return res.json([]);
    }

    try {
        const client = await pool.connect();
        const query = `
            SELECT 
                a.name, 
                a.times_played, 
                aa.average_placement, 
                ap2.average_placement AS placement_2_1, 
                ap3.average_placement AS placement_3_2, 
                ap4.average_placement AS placement_4_2
            FROM tft_schema.augments a
            LEFT JOIN tft_schema.augment_average_placement aa ON a.augment_id = aa.augment_id
            LEFT JOIN tft_schema.augment_phase_placement ap2 ON a.augment_id = ap2.augment_id AND ap2.phase = '2-1'
            LEFT JOIN tft_schema.augment_phase_placement ap3 ON a.augment_id = ap3.augment_id AND ap3.phase = '3-2'
            LEFT JOIN tft_schema.augment_phase_placement ap4 ON a.augment_id = ap4.augment_id AND ap4.phase = '4-2'
            WHERE LOWER(a.name) LIKE LOWER($1);
        `;
        const result = await client.query(query, [`%${searchTerm}%`]);
        res.json(result.rows);
        client.release();
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: err.message });
    }
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
