/**
 * Stack for the unauthenticated flow: welcome -> signup -> verify, or
 * welcome -> login.
 *
 * Headers are hidden because each screen draws its own. The root layout
 * decides whether this group is reachable at all — see the
 * `Stack.Protected` guard in `_layout.tsx`.
 */
import { Stack } from 'expo-router';

export default function AuthLayout() {
  return <Stack screenOptions={{ headerShown: false }} />;
}
