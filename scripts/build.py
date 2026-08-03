"""Regenerate every profile asset with one command.

Runs each generator from the repository root (scripts assume repo-relative
paths). Steps are independent: a failure is reported and the build continues,
so a missing photo or a network hiccup won't block the rest.

Usage:
    python scripts/build.py            # run everything
    python scripts/build.py --skip-fetch   # reuse existing contributions.json
"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"

# (label, script, optional) -- optional steps only warn on failure.
STEPS = [
    ("Prep photo", "prep_photo.py", True),
    ("Header", "make_header_svg.py", False),
    ("ASCII portrait", "make_ascii_svg.py", True),
    ("Info card", "make_card_svg.py", False),
    ("Fetch contributions", "fetch_contributions.py", True),
    ("Heatmap", "render_heatmap_svg.py", True),
    ("Footer", "make_footer_svg.py", False),
]


def run(script: str) -> bool:
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / script)],
        cwd=REPO,
    )
    return result.returncode == 0


def main() -> None:
    skip_fetch = "--skip-fetch" in sys.argv
    failures = []

    for label, script, optional in STEPS:
        if skip_fetch and script == "fetch_contributions.py":
            print(f"\n== {label}: skipped (--skip-fetch) ==")
            continue

        print(f"\n== {label} ==")
        if run(script):
            continue

        if optional:
            print(f"  ! {label} failed (optional) -- continuing")
        else:
            print(f"  ! {label} FAILED")
            failures.append(label)

    print("\n" + "=" * 40)
    if failures:
        print(f"Build finished with errors in: {', '.join(failures)}")
        sys.exit(1)
    print("Build complete.")


if __name__ == "__main__":
    main()
