const cron = require('node-cron');
const scrapeAndProcess = require('./path-to-your-scrape-and-process-function');

// Schedule tasks to be run every 2 hours
cron.schedule('0 */2 * * *', () => {
  console.log('Running scheduled tasks...');
  scrapeAndProcess(); // Function that orchestrates scraping, data insertion, and stat calculations
});
