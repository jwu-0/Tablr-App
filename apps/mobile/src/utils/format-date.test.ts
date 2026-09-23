/**
 * Tests for date formatting.
 *
 * `daysFromNow` takes `now` as an argument precisely so it can be
 * tested without freezing the clock — keep it that way.
 */
import { daysFromNow, formatTableTime } from './format-date';

describe('formatTableTime', () => {
  it('returns an empty string for an unparseable value', () => {
    expect(formatTableTime('not a date')).toBe('');
  });

  it('formats a valid ISO timestamp', () => {
    expect(formatTableTime('2026-09-26T19:30:00Z', 'en-GB')).not.toBe('');
  });
});

describe('daysFromNow', () => {
  it('counts whole days forward', () => {
    const now = new Date('2026-09-22T12:00:00Z');
    expect(daysFromNow('2026-09-25T12:00:00Z', now)).toBe(3);
  });

  it('is negative in the past', () => {
    const now = new Date('2026-09-22T12:00:00Z');
    expect(daysFromNow('2026-09-20T12:00:00Z', now)).toBe(-2);
  });
});
