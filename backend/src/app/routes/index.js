const express = require("express");
const router = express.Router();

const apiError = require("../utils/error.utils");

const multer = require("multer");
const storage = multer.diskStorage({
  destination: function (req, file, cd) {
    cd(null, './public/uploads/');
  },
  filename: function (req, file, cd) {
    cd(null, new Date().toISOString() + file.originalname)
  }
})
const upload = multer({ storage: storage })

// require controllers
const controller = require("../controllers/app.controller");

// use routes
router.route("/")
  .post(upload.single('myFile'), controller.upload)

router.use((req, res, next) => {
  return next(new apiError(404, "Resource not found"));
});

module.exports = router;