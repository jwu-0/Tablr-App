// Lets TypeScript resolve the side-effect `import '../../global.css'`.
// `expo-env.d.ts` would cover this, but it is generated and gitignored, so CI
// never has it.
declare module '*.css';
