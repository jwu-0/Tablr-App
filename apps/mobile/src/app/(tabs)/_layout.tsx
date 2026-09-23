import { NativeTabs } from 'expo-router/unstable-native-tabs';
import { brand } from '@/lib/theme/tokens';

/**
 * Native bottom tab bar (iOS/Android). The web build uses `_layout.web.tsx`.
 *
 * Note: the wireframes call for a raised, prominent centre "Add" button. Native tab
 * bars don't support a raised centre item, so "Add" is a normal trigger with a
 * filled plus glyph and the brand tint. If the raised FAB turns out to matter,
 * swap NativeTabs for JS `Tabs` with a custom `tabBarButton` — but that loses
 * the iOS 26 liquid-glass bar.
 */
export default function TabsLayout() {
  return (
    <NativeTabs tintColor={brand.green} minimizeBehavior="onScrollDown">
      <NativeTabs.Trigger name="discover">
        <NativeTabs.Trigger.Icon sf={{ default: 'fork.knife', selected: 'fork.knife' }} md="restaurant" />
        <NativeTabs.Trigger.Label>Discover</NativeTabs.Trigger.Label>
      </NativeTabs.Trigger>

      <NativeTabs.Trigger name="tables">
        <NativeTabs.Trigger.Icon sf={{ default: 'person.2', selected: 'person.2.fill' }} md="groups" />
        <NativeTabs.Trigger.Label>My Tables</NativeTabs.Trigger.Label>
      </NativeTabs.Trigger>

      <NativeTabs.Trigger name="add">
        <NativeTabs.Trigger.Icon sf="plus.circle.fill" md="add_circle" />
        <NativeTabs.Trigger.Label>Add</NativeTabs.Trigger.Label>
      </NativeTabs.Trigger>

      <NativeTabs.Trigger name="friends">
        <NativeTabs.Trigger.Icon sf={{ default: 'heart', selected: 'heart.fill' }} md="favorite" />
        <NativeTabs.Trigger.Label>Friends</NativeTabs.Trigger.Label>
      </NativeTabs.Trigger>

      <NativeTabs.Trigger name="profile">
        <NativeTabs.Trigger.Icon
          sf={{ default: 'person.crop.circle', selected: 'person.crop.circle.fill' }}
          md="account_circle"
        />
        <NativeTabs.Trigger.Label>Profile</NativeTabs.Trigger.Label>
      </NativeTabs.Trigger>
    </NativeTabs>
  );
}
