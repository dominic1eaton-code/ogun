#!/usr/bin/env python3
"""
update_version.py - Update VERSION.md files with a new semver version string,
optionally across subdirectories, and git tag the repo (and submodules).

Usage:
    python update_version.py --version 0.1.0-alpha.2
    python update_version.py --version 0.2.0 --path /my/project --depth 2
    python update_version.py --version 1.0.0 --depth 0 --no-git-tag --no-submodules
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Semver helpers
# ---------------------------------------------------------------------------

SEMVER_RE = re.compile(
    r"""
    (?P<major>0|[1-9]\d*)
    \.(?P<minor>0|[1-9]\d*)
    \.(?P<patch>0|[1-9]\d*)
    (?:-(?P<pre>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?
    (?:\+(?P<build>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?
    """,
    re.VERBOSE,
)


def is_valid_semver(version: str) -> bool:
    """Return True if *version* is a valid semver string."""
    return bool(SEMVER_RE.fullmatch(version.strip()))


def find_semver_in_content(content: str) -> list[str]:
    """Return all semver strings found in *content*."""
    return SEMVER_RE.findall(content)  # list of tuples – only used for presence check


def content_has_semver(content: str) -> bool:
    return bool(SEMVER_RE.search(content))


# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------

def find_version_files(root: Path, depth: int) -> list[Path]:
    """
    Recursively collect VERSION.md files under *root* up to *depth* levels deep.
    depth=0 means root only; depth=1 means root + immediate children, etc.
    """
    found: list[Path] = []

    def _walk(directory: Path, current_depth: int) -> None:
        candidate = directory / "VERSION.md"
        if candidate.is_file():
            found.append(candidate)

        if current_depth < depth:
            try:
                for child in sorted(directory.iterdir()):
                    if child.is_dir() and not child.name.startswith("."):
                        _walk(child, current_depth + 1)
            except PermissionError:
                pass

    _walk(root, 0)
    return found


def update_version_file(path: Path, new_version: str, dry_run: bool) -> bool:
    """
    Replace every semver string found in *path* with *new_version*.
    Returns True if the file was (or would be) changed.
    """
    content = path.read_text(encoding="utf-8")
    if not content_has_semver(content):
        print(f"  [skip]    {path}  (no semver found)")
        return False

    new_content = SEMVER_RE.sub(new_version, content)
    if new_content == content:
        print(f"  [no-op]   {path}  (version already up-to-date)")
        return False

    if dry_run:
        print(f"  [dry-run] {path}  (would update)")
    else:
        path.write_text(new_content, encoding="utf-8")
        print(f"  [updated] {path}")
    return True


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def is_git_repo(path: Path) -> bool:
    result = run_git(["rev-parse", "--is-inside-work-tree"], path)
    return result.returncode == 0


def get_git_root(path: Path) -> Path | None:
    result = run_git(["rev-parse", "--show-toplevel"], path)
    if result.returncode == 0:
        return Path(result.stdout.strip())
    return None


def get_submodule_paths(repo_root: Path) -> list[Path]:
    """Return absolute paths of all registered git submodules."""
    result = run_git(
        ["submodule", "foreach", "--quiet", "--recursive", "echo $displaypath"],
        repo_root,
    )
    if result.returncode != 0:
        return []
    paths = []
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if line:
            p = repo_root / line
            if p.is_dir():
                paths.append(p)
    return paths


def git_tag(repo_root: Path, tag: str, message: str, dry_run: bool) -> bool:
    """Create an annotated git tag. Returns True on success."""
    # Check if tag already exists
    check = run_git(["tag", "-l", tag], repo_root)
    if tag in check.stdout.splitlines():
        print(f"  [git]     Tag '{tag}' already exists in {repo_root}, skipping.")
        return False

    if dry_run:
        print(f"  [dry-run] Would create git tag '{tag}' in {repo_root}")
        return True

    result = run_git(["tag", "-a", tag, "-m", message], repo_root)
    if result.returncode == 0:
        print(f"  [git]     Created tag '{tag}' in {repo_root}")
        return True
    else:
        print(
            f"  [git]     ERROR tagging {repo_root}: {result.stderr.strip()}",
            file=sys.stderr,
        )
        return False


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def process_directory(
    root: Path,
    new_version: str,
    depth: int,
    dry_run: bool,
) -> int:
    """Update VERSION.md files under *root*. Returns count of updated files."""
    files = find_version_files(root, depth)
    if not files:
        print(f"  No VERSION.md files found under {root} (depth={depth})")
        return 0

    updated = 0
    for f in files:
        if update_version_file(f, new_version, dry_run):
            updated += 1
    return updated


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Update semver versions in VERSION.md files and optionally git-tag the repo.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--version",
        required=True,
        metavar="SEMVER",
        help="New semver version string, e.g. 0.1.0-alpha.2",
    )
    parser.add_argument(
        "--path",
        default=".",
        metavar="DIR",
        help="Root directory to search (default: current directory)",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=1,
        metavar="N",
        help=(
            "Subdirectory recursion depth. "
            "0 = root only, 1 = root + immediate children (default: 1)"
        ),
    )
    parser.add_argument(
        "--no-git-tag",
        dest="git_tag",
        action="store_false",
        default=True,
        help="Skip creating a git tag even if the directory is a git repo",
    )
    parser.add_argument(
        "--no-submodules",
        dest="submodules",
        action="store_false",
        default=True,
        help="Skip processing git submodules",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Show what would happen without making any changes",
    )
    parser.add_argument(
        "--tag-prefix",
        default="v",
        metavar="PREFIX",
        help="Prefix for git tags (default: 'v', producing e.g. v0.1.0-alpha.2)",
    )

    args = parser.parse_args()

    # Validate version
    if not is_valid_semver(args.version):
        parser.error(
            f"'{args.version}' does not look like a valid semver string "
            "(expected e.g. 1.2.3, 0.1.0-alpha.1, 2.0.0+build.42)."
        )

    root = Path(args.path).resolve()
    if not root.is_dir():
        parser.error(f"Path '{root}' is not a directory.")

    tag_name = f"{args.tag_prefix}{args.version}"
    tag_message = f"Release {args.version}"

    if args.dry_run:
        print("=== DRY RUN – no files will be written, no tags created ===\n")

    # -----------------------------------------------------------------------
    # 1. Update VERSION.md files in the main directory tree
    # -----------------------------------------------------------------------
    print(f"Searching for VERSION.md files under: {root}  (depth={args.depth})")
    updated = process_directory(root, args.version, args.depth, args.dry_run)
    print(f"\n{updated} file(s) updated in main tree.\n")

    # -----------------------------------------------------------------------
    # 2. Git operations on the main repo
    # -----------------------------------------------------------------------
    git_root: Path | None = None

    if args.git_tag and is_git_repo(root):
        git_root = get_git_root(root)
        print(f"Git repository detected: {git_root}")

        # 2a. Submodules – update VERSION.md files and tag them
        if args.submodules and git_root:
            submodule_paths = get_submodule_paths(git_root)
            if submodule_paths:
                print(f"\nFound {len(submodule_paths)} submodule(s):\n")
                for sm_path in submodule_paths:
                    print(f"  Submodule: {sm_path}")
                    sm_updated = process_directory(
                        sm_path, args.version, args.depth, args.dry_run
                    )
                    print(f"  {sm_updated} file(s) updated in submodule.\n")

                    if is_git_repo(sm_path):
                        git_tag(sm_path, tag_name, tag_message, args.dry_run)
                    else:
                        print(
                            f"  [skip]    {sm_path} is not a git repo, no tagging."
                        )
            else:
                print("No git submodules found.")

        # 2b. Tag the main repo last
        print(f"\nTagging main repository: {git_root}")
        git_tag(git_root, tag_name, tag_message, args.dry_run)

    elif args.git_tag:
        print(f"'{root}' is not inside a git repository – skipping git operations.")

    print("\nDone.")


if __name__ == "__main__":
    main()
