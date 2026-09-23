// https://docs.expo.dev/guides/using-eslint/
const { defineConfig } = require('eslint/config');
const expoConfig = require('eslint-config-expo/flat');

module.exports = defineConfig([
  expoConfig,
  {
    // Generated from packages/api-schema/openapi.json — see its README.
    ignores: ['dist/*', '.expo/*', 'src/lib/api/generated/*'],
  },
]);
