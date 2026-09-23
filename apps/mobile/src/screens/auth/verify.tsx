/**
 * Student verification gate. Unverified users can browse but not join,
 * chat, or reserve — see `require_verified` on the backend.
 * Filled in by slice 3 (verification).
 */
import { ComingSoon } from '@/components/coming-soon';

export function VerifyScreen() {
  return <ComingSoon title="Verify you're a student" note="We'll email a link to your .edu address." />;
}
