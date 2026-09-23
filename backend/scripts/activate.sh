# Sourced by the root pnpm scripts, from inside backend/.
# Activates the local virtualenv when there is one; a no-op otherwise, because
# CI installs into the runner's own Python environment.
if [ -d .venv ]; then
  . .venv/bin/activate
fi
