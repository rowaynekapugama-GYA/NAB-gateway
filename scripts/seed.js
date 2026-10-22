import { DEMO_EMAIL, DEMO_PASSWORD, seedDemo } from '../src/services/seed.js';
const created = await seedDemo();
console.log(created ? `Seeded demo business. Sign in at /login with ${DEMO_EMAIL} / ${DEMO_PASSWORD}` : 'Demo business already exists. Run `npm run reset` first to start fresh.');
