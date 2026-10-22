// Picks the right provider implementation for a business connection.
import { isDemo } from '../config.js';
import { get } from '../db.js';
import * as xeroMock from './xero/mock.js';
import * as xeroLive from './xero/live.js';
import * as gwMock from './gateway/mock.js';
import * as gwNab from './gateway/nabtransact.js';

export function xeroConnection(business_id) {
  return get('SELECT * FROM connections WHERE business_id=? AND provider=?', [business_id, 'xero']);
}
export function gatewayConnection(business_id) {
  return get('SELECT * FROM connections WHERE business_id=? AND provider=?', [business_id, 'gateway']);
}

export function xeroClient(connection) {
  if (!connection || connection.status !== 'connected') throw new Error('Xero is not connected');
  return isDemo() || connection.tenant_id?.startsWith('demo') ? xeroMock.client(connection) : xeroLive.client(connection);
}

export function gatewayClient(connection) {
  if (!connection || connection.status !== 'connected') throw new Error('Payment gateway is not connected');
  return connection.gateway_kind === 'nab_transact' ? gwNab.client(connection) : gwMock.client(connection);
}

export { xeroMock, xeroLive, gwMock, gwNab };
