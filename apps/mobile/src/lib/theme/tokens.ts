/**
 * Tablr design tokens.
 *
 * Ported from the Figma export's shadcn CSS variables and rebranded:
 *   primary    -> Tablr green
 *   background -> off-white / warm cream
 *   foreground -> near-black ink
 *
 * These are the single source of truth. `tailwind.config.js` reads them so a
 * NativeWind class (`bg-primary`) and a style value (`colors.light.primary`)
 * can never drift apart. Add a colour here first, never inline a hex.
 */

export const brand = {
  /** Tablr green — primary actions, match badges, the centre "add" button. */
  green: '#22C55E',
  greenDark: '#16A34A',
  greenLight: '#4ADE80',
  /** Page background. */
  offWhite: '#FAFAF7',
  /** Cards and raised surfaces; the "dining" warmth. */
  cream: '#FFF8F0',
  /** Text and iconography. */
  ink: '#0F0F0F',
} as const;

export type ColorTokens = {
  background: string;
  foreground: string;
  card: string;
  cardForeground: string;
  popover: string;
  popoverForeground: string;
  primary: string;
  primaryForeground: string;
  secondary: string;
  secondaryForeground: string;
  muted: string;
  mutedForeground: string;
  accent: string;
  accentForeground: string;
  destructive: string;
  destructiveForeground: string;
  border: string;
  input: string;
  ring: string;
};

const light: ColorTokens = {
  background: brand.offWhite,
  foreground: brand.ink,
  card: brand.cream,
  cardForeground: brand.ink,
  popover: '#FFFFFF',
  popoverForeground: brand.ink,
  primary: brand.green,
  primaryForeground: '#FFFFFF',
  secondary: '#F1EFE9',
  secondaryForeground: brand.ink,
  muted: '#F1EFE9',
  mutedForeground: '#6B6B66',
  accent: '#FFF8F0',
  accentForeground: brand.ink,
  destructive: '#DC2626',
  destructiveForeground: '#FFFFFF',
  border: '#E5E2DA',
  input: '#E5E2DA',
  ring: brand.green,
};

const dark: ColorTokens = {
  background: '#0F0F0F',
  foreground: '#FAFAF7',
  card: '#1A1A18',
  cardForeground: '#FAFAF7',
  popover: '#1A1A18',
  popoverForeground: '#FAFAF7',
  primary: brand.greenLight,
  primaryForeground: '#0F0F0F',
  secondary: '#262624',
  secondaryForeground: '#FAFAF7',
  muted: '#262624',
  mutedForeground: '#A3A39C',
  accent: '#262624',
  accentForeground: '#FAFAF7',
  destructive: '#EF4444',
  destructiveForeground: '#0F0F0F',
  border: '#2E2E2B',
  input: '#2E2E2B',
  ring: brand.greenLight,
};

export const colors = { light, dark } as const;

/** Figma theme used 0.625rem; RN has no rem, so 16px base -> 10px. */
export const radius = {
  sm: 6,
  md: 8,
  lg: 10,
  xl: 14,
  full: 9999,
} as const;

/** 4pt grid. */
export const spacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  '2xl': 32,
  '3xl': 48,
} as const;
