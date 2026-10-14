# Charles Zhao · Personal Website

个人网站：[zhaoshangwei.github.io](https://zhaoshangwei.github.io/)  
技术栈：Jekyll · GitHub Pages · Markdown

> **快速入口：[一键发布文章完整教程 → PUBLISHING.md](PUBLISHING.md)**

## 🚀 一键发布 Markdown 文章

在本地写完一篇文章后，运行**一条命令**，脚本就会检查文章格式、创建文章分支、提交并推送文件，以及自动创建 GitHub Pull Request。**合并 PR 后才会正式上线**，不会跳过审核直接发布。

### 1. 首次准备

安装 [Git](https://git-scm.com/)、[Python 3](https://www.python.org/downloads/) 和 [GitHub CLI (gh)](https://cli.github.com/)，然后执行：

```bash
gh auth login
git clone https://github.com/zhaoshangwei/zhaoshangwei.github.io.git
cd zhaoshangwei.github.io
```

如果已克隆仓库，先在干净的 `master` 分支执行 `git pull origin master`；无需重复克隆。

### 2. 写 Markdown 文章

在 `_posts/` 中新建 `YYYY-MM-DD-title.md`，例如：

**文件路径：** `_posts/2026-10-14-wafer-scheduling.md`

```markdown
---
layout: post
title: "半导体设备中的晶圆调度优化"
date: 2026-10-14
author: Charles Zhao
tags:
  - Semiconductor
  - Scheduling
catalog: true
mathjax: true
---

## 引言

在这里开始写作。支持 Markdown、代码块、图片及 LaTeX 数学公式。
```

文章图片可以放在 `img/posts/wafer-scheduling/` 下，通过 `/img/posts/wafer-scheduling/figure.png` 引用。

### 3. 运行一键发布

确保终端位于仓库根目录，并处于 `master` 分支、没有尚未提交的已追踪文件更改。

**macOS / Linux：**

```bash
python3 scripts/publish.py _posts/2026-10-14-wafer-scheduling.md
```

**Windows：**

```powershell
py -3 scripts/publish.py _posts/2026-10-14-wafer-scheduling.md
```

运行后脚本将：

1. 验证文件路径与文章 front matter；
2. 同步最新 `master` 并创建独立的 `post/...` 分支；
3. 只提交指定文章及与文章名称匹配的图片目录；
4. 推送分支，并使用 `gh pr create` 创建 Pull Request。

### 4. 合并并发布

打开脚本输出的 PR 链接，审核文章、图片和 CI 检查。检查通过后合并 PR，GitHub Pages 会从 `master` 更新网站。

**注意：**一键发布脚本不会自动合并 PR。运行失败时请先检查当前分支及已有 PR，不要直接重复执行。

**完整安装说明与操作细节：**[PUBLISHING.md](PUBLISHING.md)  
**一键发布脚本源文件：**[scripts/publish.py](scripts/publish.py)

## 🗂 网站结构

| 位置 | 用途 |
| --- | --- |
| `_posts/` | Markdown 技术文章 |
| `img/posts/` | 文章图片 |
| `writing/` | 文章列表 |
| `projects/` | 项目展示 |
| `research/` | 研究方向 |
| `en/` | 英文页面 |
| `_layouts/` | Jekyll 页面模板 |
| `css/` | 网站样式 |
| `.github/workflows/` | 自动化构建与质量检查 |

网站改版与维护说明见 [WEBSITE_GUIDE.md](WEBSITE_GUIDE.md)。历史文章的原始链接继续保留。

## Credits

本站基于 Jekyll 与 GitHub Pages 构建，历史站点最初参考了 [Hux Blog](https://github.com/Huxpro/huxpro.github.io) 及相关开源主题，感谢原作者。
