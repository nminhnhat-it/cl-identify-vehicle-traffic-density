const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors({ origin: 'http://localhost:3001' })).use(express.json());

// require routes
app.use("/api/", require("./routes"));

module.exports = app;