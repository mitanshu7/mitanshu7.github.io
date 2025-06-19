# Create a simple website

## Like this one

**Mitanshu Sukhwani** • _07 June 2025_

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

5. Convert the Markdown blog post to HTML using pandoc (execute in the repo folder):

   `pandoc --standalone --output html/post_title.html markdown/post_title.md`

6. Create an `index.md` file in `markdown` folder. Create the index by hyperlinking the posts:

   `1. [Post Title](html/post_title.html)`

7. Convert `index.md` to HTML using pandoc (execute in the repo folder):

   `pandoc --standalone --output index.html markdown/index.md`

   You need to create the index file at the root of your repository. Since GitHub does now allow you to host the site from folder titled other than `docs` trivially.

8. Commit, push, wait a bit, and see your website live!

### For more information, see [GitHub Pages documentation ](https://docs.github.com/en/pages)
