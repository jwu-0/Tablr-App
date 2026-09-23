/**
 * Brand typefaces, loaded from Google Fonts at runtime by `expo-font`.
 *
 *   Bebas Neue       — headlines, match percentages, big numbers
 *   DM Sans          — body, labels, buttons
 *   Playfair Display — pull quotes and editorial moments
 *
 * The keys below are the family names Tailwind refers to (see the `fontFamily`
 * block in tailwind.config.js) and must stay in sync with it.
 */
import { BebasNeue_400Regular } from '@expo-google-fonts/bebas-neue';
import {
  DMSans_400Regular,
  DMSans_500Medium,
  DMSans_700Bold,
} from '@expo-google-fonts/dm-sans';
import { PlayfairDisplay_400Regular_Italic } from '@expo-google-fonts/playfair-display';
import { useFonts } from 'expo-font';

export const fontFamily = {
  display: 'BebasNeue-Regular',
  body: 'DMSans-Regular',
  bodyMedium: 'DMSans-Medium',
  bodyBold: 'DMSans-Bold',
  quote: 'PlayfairDisplay-Italic',
} as const;

export type FontFamily = (typeof fontFamily)[keyof typeof fontFamily];

const FONT_MAP = {
  [fontFamily.display]: BebasNeue_400Regular,
  [fontFamily.body]: DMSans_400Regular,
  [fontFamily.bodyMedium]: DMSans_500Medium,
  [fontFamily.bodyBold]: DMSans_700Bold,
  [fontFamily.quote]: PlayfairDisplay_400Regular_Italic,
};

/** Blocks the first render until the brand faces are available. */
export function useBrandFonts(): { loaded: boolean; error: Error | null } {
  const [loaded, error] = useFonts(FONT_MAP);
  return { loaded, error };
}
