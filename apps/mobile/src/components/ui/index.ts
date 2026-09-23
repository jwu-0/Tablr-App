/**
 * Barrel for the design-system primitives.
 *
 * Import from here (`@/components/ui`) rather than reaching for the
 * individual files, so the public surface of the design system is one
 * list. Anything not exported here is an implementation detail.
 *
 * These five are the base set. Extend a primitive's variant map before
 * adding a sixth — a one-off styled View at a call site is how a design
 * system drifts.
 */
export { Avatar } from './avatar';
export { Button } from './button';
export { Card } from './card';
export { Input } from './input';
export { Tag } from './tag';
