import { Redirect } from 'expo-router';
import { useAuth } from '@/hooks/use-auth';

/** Entry point: hand off to the tabs or to the welcome screen. */
export default function Index() {
  const { user } = useAuth();
  return <Redirect href={user ? '/(tabs)/discover' : '/(auth)/welcome'} />;
}
