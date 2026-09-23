"""Write the OpenAPI schema to packages/api-schema/openapi.json.

That file is the contract. Run this — via `pnpm codegen` from the repo
root — after changing any router or schema, then commit the schema and
the regenerated TS client together.

    python scripts/export_openapi.py
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "backend"
OUTPUT = REPO_ROOT / "packages" / "api-schema" / "openapi.json"

sys.path.insert(0, str(BACKEND_ROOT))

from app.main import create_app  # noqa: E402


def main() -> int:
    """Write the schema and report where it went."""
    schema = create_app().openapi()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    # Stable formatting, so a diff shows a real contract change rather
    # than key-ordering churn.
    OUTPUT.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")
    print(
        f"wrote {OUTPUT.relative_to(REPO_ROOT)} ({len(schema['paths'])} paths)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
