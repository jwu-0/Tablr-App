import { TabList, TabSlot, TabTrigger, Tabs } from 'expo-router/ui';
import { Text, View } from 'react-native';

/**
 * Web shell: a persistent left side-nav instead of a bottom tab bar.
 * `expo-router/ui` gives unstyled headless tabs, so this is plain RN views.
 *
 * STUB: no icons, no active state styling yet. Route names must match the files in `(tabs)/`.
 */
const NAV = [
  { name: 'discover', href: '/discover', label: 'Discover' },
  { name: 'tables', href: '/tables', label: 'My Tables' },
  { name: 'add', href: '/add', label: 'Add a Table' },
  { name: 'friends', href: '/friends', label: 'Friends' },
  { name: 'profile', href: '/profile', label: 'Profile' },
] as const;

export default function TabsWebLayout() {
  return (
    <Tabs className="flex-1 flex-row bg-background">
      <TabList className="w-60 gap-1 border-r border-border bg-card px-3 py-6">
        <Text className="mb-6 px-3 font-display text-3xl text-foreground">Tablr</Text>
        {NAV.map((item) => (
          <TabTrigger key={item.name} name={item.name} href={item.href} className="rounded-lg px-3 py-2.5">
            <Text className="font-body text-base text-foreground">{item.label}</Text>
          </TabTrigger>
        ))}
      </TabList>
      <View className="flex-1">
        <TabSlot />
      </View>
    </Tabs>
  );
}
