require("dotenv").config();

const app = require("./app/app");
const config = require("./config");

function startServer() {
    const port = config.app.port;
    app.listen(port, () => {
      console.log(`Server is running on port ${port}`);
    });
}

startServer();