const sqlite = require('sqlite-async');

class Database {
	constructor(db_file) {
		this.db_file = db_file;
		this.db = undefined;
	}
	
	async connect() {
		this.db = await sqlite.open(this.db_file);
	}

	async migrate() {
		return this.db.exec(`
            DROP TABLE IF EXISTS paste;

            CREATE TABLE IF NOT EXISTS paste (
                id        VARCHAR(255) NOT NULL PRIMARY KEY,
                value     TEXT NOT NULL
            );
        `);
	}

	async newPaste(id, paste) {
		return new Promise(async (resolve, reject) => {
			try {
				let stmt = await this.db.prepare('INSERT INTO paste (id, value) VALUES ( ?, ? )');
				resolve((await stmt.run(id, paste)));
			} catch(e) {
				reject(e);
			}
		});
	}

	async getPaste(id) {
		return new Promise(async (resolve, reject) => {
			try {
				let stmt = await this.db.prepare('SELECT value FROM paste WHERE id = ?');
				resolve(await stmt.get(id));
			} catch(e) {
				reject(e);
			}
		});
	}

}

module.exports = Database;