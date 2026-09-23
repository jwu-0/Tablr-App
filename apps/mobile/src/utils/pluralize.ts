/** "1 seat" / "3 seats", without pulling in an i18n library yet. */
export function pluralize(count: number, singular: string, plural = `${singular}s`): string {
  return `${count} ${count === 1 ? singular : plural}`;
}
