/**
 * Auth session state for the whole app.
 *
 * STUB: holds no real session yet. Slice 1 (accounts + auth) replaces the body
 * with `supabase.auth.getSession()` + `onAuthStateChange`. The shape of the
 * context is what the rest of the app codes against, so keep it stable.
 */
import { createContext, useContext, useMemo, useState, type PropsWithChildren } from 'react';

export type AuthUser = {
  id: string;
  email: string;
  /** .edu verification gate — blocks join/chat/reserve until true. */
  isVerified: boolean;
};

export type AuthContextValue = {
  user: AuthUser | null;
  /** Raw Supabase access token, attached to every backend request. */
  accessToken: string | null;
  /** True until the persisted session has been read from storage. */
  isLoading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: PropsWithChildren) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      accessToken,
      // TODO(slice-1): start `true` and flip once the stored session resolves.
      isLoading: false,
      async signIn() {
        // TODO(slice-1): supabase.auth.signInWithPassword
        setUser(null);
        setAccessToken(null);
      },
      async signUp() {
        // TODO(slice-1): supabase.auth.signUp
      },
      async signOut() {
        // TODO(slice-1): supabase.auth.signOut
        setUser(null);
        setAccessToken(null);
      },
    }),
    [user, accessToken]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside <AuthProvider>');
  return ctx;
}
