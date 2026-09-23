/**
 * Resolves the active colour scheme to the Tablr token set.
 */
import { useColorScheme } from 'react-native';
import { colors, type ColorTokens } from '@/lib/theme/tokens';

export function useTheme(): { scheme: 'light' | 'dark'; colors: ColorTokens } {
  const scheme = useColorScheme() === 'dark' ? 'dark' : 'light';
  return { scheme, colors: colors[scheme] };
}
