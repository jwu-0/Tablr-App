/** Avatar — profile image with initials fallback. */
import { Image } from 'expo-image';
import { Text, View } from 'react-native';

const SIZE = { sm: 32, md: 44, lg: 64 } as const;

export type AvatarProps = {
  uri?: string | null;
  name?: string;
  size?: keyof typeof SIZE;
};

function initials(name?: string) {
  if (!name) return '?';
  return name
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((w) => w[0]?.toUpperCase() ?? '')
    .join('');
}

export function Avatar({ uri, name, size = 'md' }: AvatarProps) {
  const px = SIZE[size];

  if (uri) {
    return (
      <Image
        source={{ uri }}
        style={{ width: px, height: px, borderRadius: px / 2 }}
        contentFit="cover"
        accessibilityLabel={name ? `${name}'s avatar` : 'Avatar'}
      />
    );
  }

  return (
    <View
      className="items-center justify-center bg-secondary"
      style={{ width: px, height: px, borderRadius: px / 2 }}
    >
      <Text className="font-body-bold text-secondary-foreground" style={{ fontSize: px * 0.36 }}>
        {initials(name)}
      </Text>
    </View>
  );
}
