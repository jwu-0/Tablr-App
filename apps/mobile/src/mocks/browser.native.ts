/**
 * Starts MSW on iOS and Android by patching `fetch`. The web counterpart is
 * `browser.ts`, which uses a Service Worker instead.
 */
import { handlers } from './handlers';

let started = false;

export async function startMocks(): Promise<void> {
  if (started || process.env.EXPO_PUBLIC_API_MODE !== 'mock') return;
  started = true;

  const { setupServer } = await import('msw/native');
  setupServer(...handlers).listen({ onUnhandledRequest: 'bypass' });

  console.log('[msw] mock API active — no backend required');
}
