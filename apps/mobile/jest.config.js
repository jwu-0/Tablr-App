/**
 * Jest configuration.
 *
 * `jest-expo` provides the React Native transform and module mocks.
 * Tests live beside the code they cover as `*.test.ts(x)`.
 */
/** @type {import('jest').Config} */
module.exports = {
  preset: 'jest-expo',
  testMatch: ['**/*.test.ts', '**/*.test.tsx'],
  // Generated code is not ours to test.
  testPathIgnorePatterns: ['/node_modules/', '/src/lib/api/generated/'],
};
