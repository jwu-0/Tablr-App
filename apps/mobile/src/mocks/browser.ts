/**
 * Starts MSW on **web** (Service Worker). Native uses `browser.native.ts` —
 * Metro picks the right file by platform, which keeps `msw/native` out of the
 * web bundle and vice versa.
 *
 * Called once from the root layout; a no-op unless
 * `EXPO_PUBLIC_API_MODE=mock`.
 *
 * The worker file lives at `public/mockServiceWorker.js`. Regenerate it with
 * `npx msw init public/` after upgrading msw.
 */
import { handlers } from './handlers';

let started = false;

export async function startMocks(): Promise<void> {
  if (started || process.env.EXPO_PUBLIC_API_MODE !== 'mock') return;
  started = true;

  const { setupWorker } = await import('msw/browser');
  await setupWorker(...handlers).start({ onUnhandledRequest: 'bypass' });

  console.log('[msw] mock API active — no backend required');
}
