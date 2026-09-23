/**
 * The signed-in user's Tablr profile (from the backend), as opposed to the
 * Supabase auth record exposed by `useAuth`.
 *
 * STUB: returns nothing until slice 2 (profiles) wires `GET /me`.
 */
import { useAuth } from './use-auth';

export type CurrentUser = {
  id: string;
  displayName: string;
  isVerified: boolean;
};

export function useCurrentUser(): { user: CurrentUser | null; isLoading: boolean } {
  const { user, isLoading } = useAuth();
  // TODO(slice-2): replace with a query against GET /me.
  return { user: user ? { id: user.id, displayName: '', isVerified: user.isVerified } : null, isLoading };
}
