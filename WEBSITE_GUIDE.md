# Charles Zhao · Personal Website

A minimal academic personal website on Jekyll + GitHub Pages.

## Page map

- Chinese: `/`, `/about/`, `/research/`, `/projects/`, `/writing/`, `/life/`
- English: `/en/` and matching subpages
- Older blog articles keep their original paths

## Publishing an article

Create a UTF-8 Markdown document in `_posts/` named `YYYY-MM-DD-topic.md`. Use the following front matter:

~~~yaml
---
layout: post
title: "Article title"
date: 2026-10-09
author: Charles
tags:
  - Control
  - Optimization
catalog: true
mathjax: true
---
~~~

Write in Markdown. A table of contents is generated from h2 and h3 headings when `catalog: true`. The `mathjax` flag loads typesetting for mathematical formulas.

Check company confidentiality, third-party materials, links, and family privacy before publishing.

## Source layout

- Main template: `_layouts/portfolio.html`
- Long-form template: `_layouts/post.html`
- Styling: `css/portfolio.css`
- Local article filtering: `js/writing-search.js`
- Project concept illustrations: `img/portfolio/*.svg`
- SEO: `sitemap.xml` and `robots.txt`

Chinese and English overview pages have separate content. Existing technical articles are intentionally retained in their original languages, and no machine translation is implied.

## Safe deployment

The redesign stays in a review branch. Check the GitHub Actions build job, mobile display, navigation, formulas, old article links and public descriptions before merging into `master`.
