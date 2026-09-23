/**
 * The typed backend client.
 *
 * Everything the app knows about Tablr's data goes through here. Types come
 * from `generated/schema.ts`, which is produced from the backend's OpenAPI
 * document — so a backend change that breaks the app breaks the typecheck.
 *
 * Three modes, chosen by `EXPO_PUBLIC_API_MODE`:
 *   mock        — MSW intercepts; no backend, no secrets (the default)
 *   local       — http://localhost:8000
 *   staging/... — whatever EXPO_PUBLIC_API_URL points at
 */
import createClient, { type Middleware } from 'openapi-fetch';
import { getAccessToken } from '@/lib/supabase/client';
import type { paths } from './generated/schema';

export type ApiMode = 'mock' | 'local' | 'staging' | 'production';

export const apiMode = (process.env.EXPO_PUBLIC_API_MODE ?? 'mock') as ApiMode;

const DEFAULT_URLS: Record<ApiMode, string> = {
  mock: 'http://localhost:8000',
  local: 'http://localhost:8000',
  staging: '',
  production: '',
};

export const baseUrl = process.env.EXPO_PUBLIC_API_URL || DEFAULT_URLS[apiMode];

/** Attaches the Supabase JWT. The backend derives identity from it — the app
 *  never sends a user id it made up itself. */
const authMiddleware: Middleware = {
  async onRequest({ request }) {
    const token = await getAccessToken();
    if (token) request.headers.set('Authorization', `Bearer ${token}`);
    return request;
  },
};

export const api = createClient<paths>({ baseUrl: `${baseUrl}/v1` });
api.use(authMiddleware);

/** The error envelope every backend error uses (see backend/app/core/errors.py). */
export type ApiError = {
  error: { code: string; message: string };
};

export function isApiError(value: unknown): value is ApiError {
  return (
    typeof value === 'object' &&
    value !== null &&
    'error' in value &&
    typeof (value as ApiError).error?.code === 'string'
  );
}

export type { paths } from './generated/schema';
