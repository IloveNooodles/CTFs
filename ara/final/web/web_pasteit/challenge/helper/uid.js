const crypto = require("crypto");

module.exports = {
    generate() {
        return crypto.randomBytes(16).toString("hex");
    }
}