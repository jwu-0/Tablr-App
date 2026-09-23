/**
 * Route: /profile
 *
 * Thin by design — a route file only declares that the path exists and
 * points at its screen. UI, state, and data fetching live in
 * `src/screens/`, which keeps them testable and reusable across the
 * native and web shells. Do not add anything else here.
 */
export { ProfileScreen as default } from '@/screens/profile';
