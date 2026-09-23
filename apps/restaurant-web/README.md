# restaurant-web — placeholder

The restaurant partner portal. React web app, built after the student app's
core loop closes — see [TABLR_PLAN.md](../../TABLR_PLAN.md).

Nothing here yet. It is a separate app rather than a route in `apps/mobile`
because partners and students share almost no UI, and the portal will need
desktop-first layouts, staff roles, and a different auth surface.

When it starts:

- It talks to the same Python backend through the same generated client.
- It gets its own `package.json` and joins the pnpm workspace automatically.
- Restaurant-owned data ends up in `backend/app/domains/restaurants/`.
