/**
 * Placeholder body for every screen that has not been built yet.
 * Delete the usage as each vertical slice lands.
 */
import { Text, View } from 'react-native';

export function ComingSoon({ title, note }: { title: string; note?: string }) {
  return (
    <View className="flex-1 items-center justify-center gap-2 bg-background px-6">
      <Text className="font-display text-3xl text-foreground">{title}</Text>
      <Text className="text-center font-body text-base text-muted-foreground">
        {note ?? 'Coming soon.'}
      </Text>
    </View>
  );
}
