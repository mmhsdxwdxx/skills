#!/usr/bin/env python3
"""Public entry point for the official-document PDF generator.

All layout and rendering logic lives in ``_official_pdf_impl``; this thin runner
keeps ``python scripts/official_pdf.py`` as the documented invocation while
ensuring there is exactly one implementation of every function.
"""

from __future__ import annotations

import _official_pdf_impl as impl


if __name__ == "__main__":
    raise SystemExit(impl.main())
