This documents the current setup and codebase backing aggressivelyparaphrasing.me.

# Code

This website is mostly a static website backed by [hugo](https://gohugo.io).  I chose hugo because of the easy installation, and the relatively straight forward structure and flexibility.

I intend to build a custom [flask](http://flask.pocoo.org) web server in this same repository to function as a Web UI frontend that drives the hugo CLI, allowing me to blog without needing to mess with the server or the CLI directly.  My primary motivation was to blog with my phone.

I intend to build my own theme because I'm like that.

# How It Was Made

```
$ hugo new site hugo/
$ cd hugo/
$ hugo new theme aggpara
$ echo 'theme = "aggpara"' >> config.toml
```

Then I read through the [homepage content generation article](https://gohugo.io/templates/homepage/).  This means create the `themes/aggpara/layouts/index.html` from that documentation as is.

Then I created content for the homepage with: `hugo new _index.md`

For my personal sanity, I finally understood:
* It's a good idea to just create your own theme.  This allows you to separate your "content" from your "presentation"
* You can always add a theme under your theme
* The theme generation gives you nice starting defaults.
* baseof.html contains the generic layout (head, header, body, footer)
* head.html is the `<head>` content for metadata stuff
* header.html appears above all pages
* footer.html is below
* index.html "defines main" for baseof.html to fill the content with

Honestly, I felt like I never really learned HTML deeply until I read [Mozilla's guide](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML).  It's very thorough.  I chose this because there was an article on Lobste.rs that mentioned people should just learn all 150 tags in HTML, they're not that many and they provide a lot of useful built-in features from the browser.

While going through the mozilla tutorial, I felt like I needed a sample.md file to visually see how I would style all my content, from one page.  That way, I can pick the overall style of my site without having to view all my individual pages to see how it all fits together.

# Server

Although not set up yet, I intend to:
1. get the domain from NameCheap
2. set up the SSL certificate with LetsEncrypt
3. set up hosting from https://www.nearlyfreespeech.net
4. set up email from mxroute.com
5. Set up mail forwarding from DNS