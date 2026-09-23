# features/

Client-side feature logic, mirroring the backend domains one-for-one. This is
where queries, mutations, and view-model shaping live — *not* business rules.

Rule of thumb: if the answer would change based on data the client cannot see,
it belongs in `backend/app/domains/<same-name>/service.py`. Match scoring, who
may join a table, and whether a reservation may advance are all backend
decisions. Formatting, caching, optimistic updates, and derived display state
are frontend ones.

Each folder gets `queries.ts` (react-query hooks over `@/lib/api`) and, where
useful, `types.ts` re-exporting the generated schema types under friendlier
names.
