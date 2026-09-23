import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useEffect, useState } from 'react';
import { AppProviders } from '@/providers';
import { useAuth } from '@/hooks/use-auth';
import { useBrandFonts } from '@/lib/theme/fonts';
import { startMocks } from '@/mocks/browser';
import '../../global.css';

export default function RootLayout() {
  // In mock mode nothing may hit the network before MSW is listening.
  const mocksReady = useMocks();
  if (!mocksReady) return null;

  return (
    <AppProviders>
      <StatusBar style="auto" />
      <RootNavigator />
    </AppProviders>
  );
}

/** Resolves once MSW is listening (or immediately outside mock mode). */
function useMocks(): boolean {
  const [ready, setReady] = useState(process.env.EXPO_PUBLIC_API_MODE !== 'mock');

  useEffect(() => {
    if (ready) return;
    startMocks()
      .catch((error) => console.warn('[msw] failed to start', error))
      .finally(() => setReady(true));
  }, [ready]);

  return ready;
}

/**
 * The auth gate. `Stack.Protected` keeps unauthenticated users out of `(tabs)`
 * and signed-in users out of `(auth)` — no imperative redirects needed.
 */
function RootNavigator() {
  const { user, isLoading } = useAuth();
  const { loaded: fontsLoaded } = useBrandFonts();

  // TODO(phase-1): hold the splash screen instead of rendering nothing.
  if (isLoading || !fontsLoaded) return null;

  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Protected guard={!!user}>
        <Stack.Screen name="(tabs)" />
      </Stack.Protected>
      <Stack.Protected guard={!user}>
        <Stack.Screen name="(auth)" />
      </Stack.Protected>
    </Stack>
  );
}
