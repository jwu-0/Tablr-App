/**
 * MSW request handlers.
 *
 * These let the app run with **no backend and no secrets** — which is how the
 * frontend work gets done. Every handler's shape must match the OpenAPI
 * contract; if a response here does not typecheck against `paths`, the mock is
 * lying and the real screen will break.
 *
 * STUB: mostly empty collections. Fill in realistic fixtures as each slice
 * lands, so the screens have something to render.
 */
import { HttpResponse, http } from 'msw';
import { baseUrl } from '@/lib/api';

const v1 = (path: string) => `${baseUrl}/v1${path}`;

export const handlers = [
  http.get(`${baseUrl}/health`, () => HttpResponse.json({ status: 'ok', environment: 'mock' })),

  // --- identity ------------------------------------------------------------
  http.get(v1('/me'), () =>
    HttpResponse.json({
      id: 'mock-user',
      email: 'ada@example.edu',
      display_name: 'Ada',
      is_verified: true,
      created_at: new Date().toISOString(),
    })
  ),

  // --- verification --------------------------------------------------------
  http.get(v1('/verification/status'), () => HttpResponse.json({ status: 'verified' })),

  // --- profiles + taxonomy -------------------------------------------------
  http.get(v1('/tags'), () => HttpResponse.json([])),
  http.get(v1('/profiles/:profileId'), ({ params }) =>
    HttpResponse.json({ id: params.profileId, is_verified: true, tags: [] })
  ),

  // --- restaurants ---------------------------------------------------------
  http.get(v1('/restaurants'), () => HttpResponse.json({ items: [], next_cursor: null })),

  // --- tables --------------------------------------------------------------
  http.get(v1('/tables'), () => HttpResponse.json({ items: [], next_cursor: null })),
  http.get(v1('/me/tables'), () => HttpResponse.json({ items: [], next_cursor: null })),

  // --- matching ------------------------------------------------------------
  http.get(v1('/matching/preview'), () => HttpResponse.json({ candidates: [] })),

  // --- chat ----------------------------------------------------------------
  http.get(v1('/tables/:tableId/messages'), () =>
    HttpResponse.json({ items: [], next_cursor: null })
  ),
];
