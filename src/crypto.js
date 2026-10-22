import {
  createCipheriv, createDecipheriv, createHmac, randomBytes, scryptSync,
  timingSafeEqual, createHash,
} from 'node:crypto';
import { config } from './config.js';

const key = () => createHash('sha256').update(config.appSecret).digest();

// AES-256-GCM. Output: base64(iv).base64(tag).base64(ciphertext)
export function encrypt(plain) {
  if (plain == null) return null;
  const iv = randomBytes(12);
  const cipher = createCipheriv('aes-256-gcm', key(), iv);
  const enc = Buffer.concat([cipher.update(String(plain), 'utf8'), cipher.final()]);
  const tag = cipher.getAuthTag();
  return [iv, tag, enc].map((b) => b.toString('base64')).join('.');
}

export function decrypt(blob) {
  if (!blob) return null;
  const [iv, tag, enc] = blob.split('.').map((s) => Buffer.from(s, 'base64'));
  const decipher = createDecipheriv('aes-256-gcm', key(), iv);
  decipher.setAuthTag(tag);
  return Buffer.concat([decipher.update(enc), decipher.final()]).toString('utf8');
}

export function hashPassword(password) {
  const salt = randomBytes(16).toString('hex');
  const hash = scryptSync(password, salt, 64).toString('hex');
  return `${salt}:${hash}`;
}

export function verifyPassword(password, stored) {
  if (!stored) return false;
  const [salt, hash] = stored.split(':');
  const test = scryptSync(password, salt, 64);
  return timingSafeEqual(test, Buffer.from(hash, 'hex'));
}

export function token(bytes = 24) {
  return randomBytes(bytes).toString('base64url');
}

export function shortCode(len = 6) {
  const alphabet = 'abcdefghjkmnpqrstuvwxyz23456789';
  const b = randomBytes(len);
  return Array.from(b, (x) => alphabet[x % alphabet.length]).join('');
}

export function sign(value) {
  return createHmac('sha256', key()).update(value).digest('base64url');
}

export function verifySigned(value, sig) {
  if (!sig) return false;
  const a = Buffer.from(sign(value));
  const b = Buffer.from(sig);
  return a.length === b.length && timingSafeEqual(a, b);
}

export function sha256(s) {
  return createHash('sha256').update(s).digest('hex');
}
