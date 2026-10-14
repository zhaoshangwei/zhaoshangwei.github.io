#!/usr/bin/env python3
"""Publish a Jekyll post through a reviewable GitHub pull request.

Prerequisites: git, GitHub CLI (gh), and an authenticated gh session.
Usage: python3 scripts/publish.py _posts/YYYY-MM-DD-slug.md
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args, capture=False):
    return subprocess.run(args, cwd=ROOT, check=True, text=True,
                          capture_output=capture).stdout.strip() if capture else subprocess.run(args, cwd=ROOT, check=True)


def fail(message):
    raise SystemExit("Error: " + message)


def main():
    parser = argparse.ArgumentParser(description="Create a review PR for a Jekyll article")
    parser.add_argument("post", help="Markdown file inside _posts/, e.g. _posts/2026-10-14-my-post.md")
    args = parser.parse_args()
    for cmd in ("git", "gh"):
        if not shutil.which(cmd):
            fail(f"{cmd} is not installed")
    post = (Path.cwd() / args.post).resolve()
    try:
        relative = post.relative_to(ROOT)
    except ValueError:
        fail("Article must be inside this repository")
    if not relative.parts or relative.parts[0] != "_posts" or not re.fullmatch(r"\\d{4}-\\d{2}-\\d{2}-.+\\.(md|markdown)", post.name):
        fail("Article must be _posts/YYYY-MM-DD-title.md")
    if not post.is_file():
        fail(f"File not found: {relative}")
    content = post.read_text(encoding="utf-8-sig")
    if not content.startswith("---\n") or "\n---\n" not in content[4:]:
        fail("Article needs YAML front matter enclosed by ---")
    front = content.split("---", 2)[1]
    if not re.search(r"(?m)^title:\\s*\\S", front):
        fail("Article front matter needs a title")
    if not re.search(r"(?m)^layout:\\s*post\\s*$", front):
        fail("Article must set layout: post")
    if not re.search(r"(?m)^date:\\s*\\d{4}-\\d{2}-\\d{2}", front):
        fail("Article front matter needs date: YYYY-MM-DD")
    if run("git", "status", "--porcelain", capture=True):
        # New article and its images may be untracked, but preexisting changes cannot be auto-committed safely.
        status = run("git", "status", "--porcelain", "--untracked-files=no", capture=True)
        if status:
            fail("Tracked files have uncommitted changes. Commit/stash them first")
    branch = run("git", "branch", "--show-current", capture=True)
    if branch != "master":
        fail("Switch to master before publishing")
    run("gh", "auth", "status")
    run("git", "pull", "--ff-only", "origin", "master")
    slug = re.sub(r"[^a-z0-9-]+", "-", post.stem[11:].lower()).strip("-") or "article"
    publish_branch = "post/" + post.stem[:10] + "-" + slug
    run("git", "switch", "-c", publish_branch)
    print("Selected article:", relative)
    image_dir = ROOT / "img" / "posts" / post.stem[11:]
    run("git", "add", "--", relative.as_posix())
    if image_dir.is_dir():
        run("git", "add", "--", image_dir.relative_to(ROOT).as_posix())
    staged = run("git", "diff", "--cached", "--name-only", capture=True)
    if relative.as_posix() not in staged.splitlines():
        fail("Article was not staged; check .gitignore")
    run("git", "commit", "-m", "Add article: " + post.stem)
    run("git", "push", "-u", "origin", publish_branch)
    run("gh", "pr", "create", "--base", "master", "--head", publish_branch,
        "--title", "Publish: " + post.stem[11:],
        "--body", "New Markdown article. Review content and CI before merging.\n\n- [ ] Preview article and formulas\n- [ ] Check image paths and public disclosure")
    print("\nPR created. Merge it after CI passes to publish the article.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        fail(f"Command failed: {exc.cmd}")
