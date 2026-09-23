/**
 * Date formatting for display.
 *
 * Everything crossing the API is UTC ISO-8601. Conversion to the viewer's
 * timezone happens here and nowhere else.
 */

/** e.g. "Fri 26 Sep, 7:30 pm" in the device's locale and timezone. */
export function formatTableTime(iso: string, locale?: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return '';
  return new Intl.DateTimeFormat(locale, {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
    hour: 'numeric',
    minute: '2-digit',
  }).format(date);
}

/** Whole days from now, negative in the past. Useful for "in 3 days". */
export function daysFromNow(iso: string, now: Date = new Date()): number {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return 0;
  const msPerDay = 86_400_000;
  return Math.round((date.getTime() - now.getTime()) / msPerDay);
}
