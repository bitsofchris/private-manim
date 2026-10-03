# private-manim

Read `AGENTS.md` first. It is the single entry point: the map of this repo,
the hard rules, how a session runs, and how the repo stays clean. Nothing
in this file overrides it.

Two things that break the repo if forgotten:

- Render from inside the video folder, one scene at a time:
  `cd videos/NNN-slug && uv run --no-sync manim -qh --disable_caching FILE.py Class`
- Every scene file starts with the 3-line `sys.path` shim so
  `videos._shared` imports from inside a video folder:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared
```
