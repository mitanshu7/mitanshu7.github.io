---
# 1. Basic Identification
title: "Create a simple website"
subtitle: "**Like this one**"
author: "_Mitanshu Sukhwani_"
date: "`2025-06-07`"
lang: en

# 2. Metadata / SEO
description: "Step-by-step guide to build a free personal website using GitHub Pages and Markdown. Convert your content with Pandoc and publish easily without writing raw HTML. Ideal for developers and writers familiar with git."
keywords: "GitHub Pages, Markdown, Pandoc, HTML, website, free, personal, developer, writer, git"
---

To create a simple (and free) website we will be using [Github Pages](https://pages.github.com/).

The following assumptions are made:

1. You have working knowledge of [git](https://git-scm.com/).

2. You have a [GitHub](https://github.com/) account.

3. You are more comfortable with [Markdown](https://www.markdownguide.org/) than [HTML](https://www.w3schools.com/html/).

# Steps

1. Follow the steps on [GitHub Pages](https://pages.github.com/) to have a initial functional website.

2. Install [pandoc](https://pandoc.org/) from [here](https://pandoc.org/installing.html) for your operating system. Pandoc helps converting Markdown to HTML, the languge of choice for www.

3. In your git repository (better to clone and work locally) _username.github.io_, make two folders, one titled `markdown` to store markdown files and another titled `html` to store html.

4. Create a blog post in the `markdown` folder with title `post_title.md`.

5. In the top of the `post_title.md`, create a YAML front matter with the following fields:

   ```yaml
   ---
   # 1. Basic Identification
   title: Post Title
   subtitle: Post Subtitle
   author: Your Name
   date: YYYY-MM-DD
   lang: en

   # 2. Metadata / SEO
   description: Post Description
   keywords: [keyword1, keyword2, keyword3]
   ---
   ```

   to make the blog post SEO friendly. You may skip adding keywords if you don't have any. It is safer to add `""` around the values of `title`, `subtitle`, `author`, and `description` fields.

6. Convert the Markdown blog post to HTML using pandoc (execute in the repo folder):

   ```bash
   pandoc --standalone --output html/post_title.html markdown/post_title.md
   ```

7. Create an `index.md` file in `markdown` folder. Create the index by hyperlinking the posts:

   ```markdown
   1. [Post Title](html/post_title.html)
   ```

8. Convert `index.md` to HTML using pandoc (execute in the repo folder):

   ```bash
   pandoc --standalone --output index.html markdown/index.md
   ```

   You need to create the index file at the root of your repository. Since GitHub does now allow you to host the site from folder titled other than `docs` trivially.

9. Commit, push, wait a bit, and see your website live!

You can check the quality of your website on [PageSpeed Insights](https://pagespeed.web.dev/).
See [this report](https://pagespeed.web.dev/analysis/https-blog-papermatch-me/xfzuhinhkq?form_factor=mobile) for [mitanshu7.github.io](https://mitanshu7.github.io/).

Have a look at [GitHub Pages documentation](https://docs.github.com/en/pages) too.

## Bonus!

I have created a python script to convert all markdown files to html to ease the process. The script also uses `html/template.html` to add _Back to Home_ links on the bottom of every page.

Please visit [mitanshu7/mitanshu7.github.io](https://github.com/mitanshu7/mitanshu7.github.io)!

## Honorary mention

[Hugo](https://gohugo.io/) is one of the most popular open-source static site generators. Checkout their [Quick start](https://gohugo.io/getting-started/quick-start/) and [Host and deploy](https://gohugo.io/host-and-deploy/) page for a similar setup as above. It also comes with a plethora of [Themes](https://themes.gohugo.io/).
