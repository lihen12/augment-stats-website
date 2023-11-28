// cache.js
const NodeCache = require("node-cache");

// Set the standard TTL (Time To Live) for cached items to 7200 seconds (2 hours)
// Set the cache check period to 120 seconds (2 minutes)
const myCache = new NodeCache({ stdTTL: 7200, checkperiod: 120 });

module.exports = myCache;
