/**
 * Supabase client — AUTH ONLY (and, later, storage uploads).
 *
 * All business data goes through the Python backend. Do not add table queries
 * here: the backend is the single door. See CLAUDE.md.
 *
 * This client holds the **anon** key, which is public by design and safe to
 * ship in the bundle — it is constrained by row-level security. The
 * service-role key must never appear in this app.
 */
import AsyncStorage from '@react-native-async-storage/async-storage';
import { createClient } from '@supabase/supabase-js';
import { Platform } from 'react-native';

// `||` rather than `??`: an unset EXPO_PUBLIC_* var is inlined as an empty
// string, not undefined, and createClient rejects an empty URL.
const supabaseUrl = process.env.EXPO_PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY || '';

// Placeholders that let the bundle build and mock mode run with no project.
const LOCAL_SUPABASE_URL = 'http://localhost:54321';
const PLACEHOLDER_ANON_KEY = 'anon';

// Mock mode runs without a Supabase project at all, so only complain when the
// app is actually expected to reach one.
if ((!supabaseUrl || !supabaseAnonKey) && process.env.EXPO_PUBLIC_API_MODE !== 'mock') {
  console.warn(
    '[supabase] EXPO_PUBLIC_SUPABASE_URL / EXPO_PUBLIC_SUPABASE_ANON_KEY are unset. ' +
      'Auth calls will fail. Copy .env.example to .env, or run in mock mode.'
  );
}

const isWeb = Platform.OS === 'web';

export const supabase = createClient(supabaseUrl || LOCAL_SUPABASE_URL, supabaseAnonKey || PLACEHOLDER_ANON_KEY, {
  auth: {
    // Web persists to localStorage (the default); native needs explicit storage.
    storage: isWeb ? undefined : AsyncStorage,
    autoRefreshToken: true,
    persistSession: true,
    // Only the web build can read the session out of a redirect URL.
    detectSessionInUrl: isWeb,
  },
});

/** The JWT the API wrapper attaches to backend requests. */
export async function getAccessToken(): Promise<string | null> {
  const { data } = await supabase.auth.getSession();
  return data.session?.access_token ?? null;
}
