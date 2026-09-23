/**
 * Welcome — first screen an unauthenticated visitor sees.
 * Filled in by slice 1 (accounts + auth).
 */
import { Link } from 'expo-router';
import { Text, View } from 'react-native';
import { Button } from '@/components/ui/button';

export function WelcomeScreen() {
  return (
    <View className="flex-1 items-center justify-center gap-6 bg-background px-6">
      <Text className="font-display text-5xl text-foreground">Tablr</Text>
      <Text className="text-center font-body text-base text-muted-foreground">
        Good food is better with good company.
      </Text>
      <View className="w-full gap-3">
        <Link href="/(auth)/signup" asChild>
          <Button title="Create an account" />
        </Link>
        <Link href="/(auth)/login" asChild>
          <Button title="I already have one" variant="secondary" />
        </Link>
      </View>
    </View>
  );
}
