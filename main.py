#!/usr/bin/env python3
"""Copy the pre-rendered entry.png to the grader output directory.

The image was drawn offline by gen.py (PIL) from 40 source-verified
Friday 20 November 2026 news stories; this file only copies the bytes,
so both grader runs produce identical output. Standard library only.
"""
import os
import shutil


def main():
    # entry.png sits beside this file in the repository root.
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    shutil.copyfile(src, os.path.join(outdir, "entry.png"))


if __name__ == "__main__":
    main()
