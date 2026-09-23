/**
 * Tag — interest / cuisine / vibe chip.
 * `selected` is the picker state; `tone` distinguishes canonical preset tags
 * from user-requested free-text ones (see the taxonomy in the profiles domain).
 */
import { Pressable, Text } from 'react-native';

export type TagProps = {
  label: string;
  selected?: boolean;
  tone?: 'preset' | 'custom';
  onPress?: () => void;
};

export function Tag({ label, selected = false, tone = 'preset', onPress }: TagProps) {
  const base = selected
    ? 'bg-primary border-primary'
    : tone === 'custom'
      ? 'bg-transparent border-dashed border-border'
      : 'bg-secondary border-border';

  return (
    <Pressable
      accessibilityRole={onPress ? 'button' : undefined}
      accessibilityState={{ selected }}
      onPress={onPress}
      className={`rounded-full border px-md py-xs ${base}`}
    >
      <Text
        className={`font-body-medium text-sm ${selected ? 'text-primary-foreground' : 'text-foreground'}`}
      >
        {label}
      </Text>
    </Pressable>
  );
}
