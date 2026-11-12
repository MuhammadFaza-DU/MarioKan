"""Preflight satu Update File: tolak hunk no-op, konteks salah atau mundur."""

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def validate_hunks(original, hunks):
    source = original.splitlines()
    cursor = 0
    for index, hunk in enumerate(hunks, 1):
        if not any(line.startswith(("+", "-")) for line in hunk):
            raise ValueError(f"hunk {index}: no-op")
        context = [line[1:] for line in hunk if line.startswith((" ", "-"))]
        matches = [start for start in range(len(source) - len(context) + 1)
                   if source[start:start + len(context)] == context]
        following = [start for start in matches if start >= cursor]
        if not following:
            reason = "source order" if matches else "incorrect context"
            raise ValueError(f"hunk {index}: {reason}")
        cursor = following[0] + len(context)


def check_patch(patch_path):
    lines = Path(patch_path).read_text(encoding="utf-8").splitlines()
    headers = [line for line in lines if line.startswith(("*** Update File:", "*** Add File:", "*** Delete File:"))]
    if len(headers) != 1 or not headers[0].startswith("*** Update File:"):
        raise ValueError("preflight hanya menerima satu Update File per patch")
    target = (ROOT / headers[0].split(":", 1)[1].strip()).resolve()
    if not target.is_relative_to(ROOT):
        raise ValueError("target di luar project")
    hunks = []
    for line in lines[lines.index(headers[0]) + 1:]:
        if line == "*** End Patch":
            break
        if line.startswith("@@"):
            hunks.append([])
        elif hunks and line.startswith((" ", "+", "-")):
            hunks[-1].append(line)
        else:
            raise ValueError("baris/hunk patch tidak didukung preflight")
    if not hunks:
        raise ValueError("patch tanpa hunk")
    validate_hunks(target.read_text(encoding="utf-8"), hunks)
    return target.relative_to(ROOT)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("patch", type=Path)
    args = parser.parse_args()
    try:
        print("PASS patch preflight:", check_patch(args.patch))
    except (OSError, ValueError) as error:
        parser.exit(1, f"FAIL patch preflight: {error}\n")
