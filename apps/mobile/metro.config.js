const { getDefaultConfig } = require('expo/metro-config');
const { withNativeWind } = require('nativewind/metro');
const path = require('node:path');

const projectRoot = __dirname;
const workspaceRoot = path.resolve(projectRoot, '../..');

const config = getDefaultConfig(projectRoot);

// In this monorepo pnpm hoists every dependency to the workspace root
// (`nodeLinker: hoisted` in pnpm-workspace.yaml), which is outside the project
// root — so Metro has to watch it and look for modules there. Hierarchical
// lookup stays on: with a flat tree it resolves correctly on its own.
config.watchFolders = [workspaceRoot];
config.resolver.nodeModulesPaths = [
  path.resolve(projectRoot, 'node_modules'),
  path.resolve(workspaceRoot, 'node_modules'),
];

module.exports = withNativeWind(config, { input: './global.css' });
