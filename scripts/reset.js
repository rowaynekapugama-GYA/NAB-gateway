// Deletes the SQLite database so you can start from a clean slate.
import { rmSync } from 'node:fs';
import { config } from '../src/config.js';
for (const f of [config.dbPath, config.dbPath + '-wal', config.dbPath + '-shm']) rmSync(f, { force: true });
console.log('Database removed:', config.dbPath);
