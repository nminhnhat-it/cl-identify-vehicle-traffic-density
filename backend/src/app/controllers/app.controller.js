const apiError = require("../utils/error.utils");
module.exports = {

  async upload(req, res, next) {
    image_path = req.file['path'];
    const { spawn } = require("child_process");
    const pythonProcess = spawn('src/venv/bin/python', ["src/identify_vehicle_traffic_density.py", image_path]);
    pythonProcess.stdout.on('data', (data) => {
      res.send(data.toString())
      var fs = require('fs');
      var filePath = './' + image_path;
      fs.unlinkSync(filePath);
    });
  },
}