/**
 * Babel configuration.
 *
 * `jsxImportSource: 'nativewind'` is what lets `className` work on React
 * Native components; `nativewind/babel` compiles the Tailwind classes.
 * Both are required — NativeWind does not work with only one.
 */
module.exports = function (api) {
  api.cache(true);
  return {
    presets: [['babel-preset-expo', { jsxImportSource: 'nativewind' }], 'nativewind/babel'],
  };
};
