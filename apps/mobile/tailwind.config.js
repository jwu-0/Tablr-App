/**
 * Tailwind/NativeWind config.
 *
 * `src/lib/theme/tokens.ts` is the single source of truth for colour. This file
 * reads it, emits the light and dark palettes as CSS variables, and points every
 * semantic Tailwind colour at those variables — so `bg-primary` in a className
 * and `colors.light.primary` in a StyleSheet can never disagree, and both
 * schemes come from one place.
 */
const plugin = require('tailwindcss/plugin');
const { colors, radius, spacing } = require('./src/lib/theme/tokens.ts');

const kebab = (s) => s.replace(/[A-Z]/g, (c) => `-${c.toLowerCase()}`);

/** '#22C55E' -> '34 197 94' (space-separated so Tailwind can inject alpha). */
const toRgbChannels = (hex) => {
  const n = parseInt(hex.replace('#', ''), 16);
  return `${(n >> 16) & 255} ${(n >> 8) & 255} ${n & 255}`;
};

const toCssVars = (palette) =>
  Object.fromEntries(Object.entries(palette).map(([k, v]) => [`--${kebab(k)}`, toRgbChannels(v)]));

const semanticColors = Object.fromEntries(
  Object.keys(colors.light).map((k) => [kebab(k), `rgb(var(--${kebab(k)}) / <alpha-value>)`])
);

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  presets: [require('nativewind/preset')],
  darkMode: 'class',
  theme: {
    extend: {
      colors: semanticColors,
      borderRadius: Object.fromEntries(Object.entries(radius).map(([k, v]) => [k, `${v}px`])),
      spacing: Object.fromEntries(Object.entries(spacing).map(([k, v]) => [k, `${v}px`])),
      fontFamily: {
        display: ['BebasNeue-Regular'],
        body: ['DMSans-Regular'],
        'body-medium': ['DMSans-Medium'],
        'body-bold': ['DMSans-Bold'],
        quote: ['PlayfairDisplay-Italic'],
      },
    },
  },
  plugins: [
    plugin(({ addBase }) => {
      addBase({
        ':root': toCssVars(colors.light),
        // NativeWind's dark-mode selector — do not change to plain `.dark`.
        '.dark:root': toCssVars(colors.dark),
      });
    }),
  ],
};
