# One-command article publishing

The website's public name stays **Charles Zhao**.

Prerequisites: install [Git](https://git-scm.com/), [GitHub CLI](https://cli.github.com/), and Python 3; run `gh auth login` once.

1. Write `_posts/YYYY-MM-DD-title.md` containing YAML front matter with `layout: post`, `title`, and `date`.
2. Optionally store article images in `img/posts/title/` (the filename slug without its date prefix); reference as `/img/posts/title/image.png`.
3. From repository root, on a clean `master` branch, run:

```bash
python3 scripts/publish.py _posts/2026-10-14-my-article.md
```

On Windows, `py -3 scripts/publish.py _posts/2026-10-14-my-article.md` also works.

The script validates front matter, pulls the latest `master`, creates `post/YYYY-MM-DD-title`, stages only that post and its matching image directory, commits, pushes, and opens a **pull request** using GitHub CLI.

**It does not merge or directly publish.** Review the PR and CI, then merge to deploy via GitHub Pages. If anything fails, inspect the current branch and PR before retrying. Existing untracked unrelated files are never staged.
