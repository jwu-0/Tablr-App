/**
 * Money is integer minor units (cents) everywhere — in the database, in the
 * API, and in this app. It becomes a decimal exactly once, here, at the point
 * of display.
 */

export function formatCents(cents: number, currency = 'USD', locale?: string): string {
  return new Intl.NumberFormat(locale, { style: 'currency', currency }).format(cents / 100);
}

/** "about $18 a head" style rounding for price hints. */
export function formatCentsApprox(cents: number, currency = 'USD', locale?: string): string {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
    maximumFractionDigits: 0,
  }).format(Math.round(cents / 100));
}
