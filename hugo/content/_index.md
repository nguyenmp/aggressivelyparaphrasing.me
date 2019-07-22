---
title: "Aggressively Paraphrasing"
date: 2019-07-02T23:26:35-07:00
draft: true
---
## Hello world!

This is my personal website.  There are two types of content:

<dl>
<dt>Wikis</dt>
<dd>These are living documents that get updated over time.  I use them to develop my thoughts and use as references.  Generally, they're just dumps of information.</dd>
<dt>Notes</dt>
<dd>These are the "blog" of my website.  They're like mental snapshots.</dd>
</dl>

## Motivation

I have been journaling for a bit of time and Google Docs started to fail at around 200 pages.  The page itself was getting slow to load and would sometimes bug out.  It took a long time to jump between dfiferent sections of the docuemnt.  I had already transitioned to a split "wikis" versus "notes" style but it was difficult to transition between them.  The document itself didn't feel like an archive, even though I wanted it to be one.

Moreover, my hosting provider decided to shut down and I wanted to spend some time working on my site again.

## Requirements

To begin, I thought about what I really wanted out of my journaling system and website.

* **Notes vs Wikis**; I'm pretty excited to try out this idea of separating long running reference pages from instantaneious thoughts.  Unfortunately, most platforms are either blogs or wikis.
* **Mobile friendly**; I want to be able to take notes wherever I am.  An example is a friend suggests a good place to eat while we are walking in the park.  I want to be able to take that and put it into my "foods to eat" reference page.
* **Fast and scalable**; I don't want to have to wait too much on large assets, javascripts, external dependencies.  Google Docs takes a suprising amount of time when it starts scaling to the hundreds of pages.  Ideally, I can post endlessly and have dozens reference pages that are dozens of screens long.
* **Sharable**; Often times, I want to be able to share my reference pages to individuals.  Sometimes, it's a new person who wants to get into Anime so I want to share with them my top picks.
* **Searchable**; Sometimes, I have a need to go back and find some piece of information I left buried away somewhere.  Usually, they're in the reference pages, but sometimes they're just a note.  I think I will start having more in notes as I start writing responses to reading pieces.
* **Error resistant**; I'm pretty terrified of losing this data.  I can trust Google to not lose all the material I've been working on, but can I trust myself?  Revision history would be nice.
* **Fine Controls**; I want to be able to control a lot of weird aspects of my website.  After reading the Mozilla guide to web development, there's a lot of minor things I really like, like definition lists, citations to quotes, link titles, and just a very strong ability to finely adjust the design and content of my website, like the CSS, headers, footers, etc.

## Prior Works

Most existing solutions were disatisfying in some way, due to my desire to have both a "blog" and a "wiki".

* Wix and Square aren't really blogs or wikis.  The contents are pretty static and the tools to build these websites are incredibly heavy, since they're website building tools, rather than content creation tools.
* Blogger and Wordpress aren't really wikis and aren't really designed to have long lived posts/pages that are edited often.  Wordpress seems to have an Android app for posting, but it seems like a WYSIWYG editor.
* Running your own wiki seems pretty sketchy.  A lot of the software is pretty big and looks ugly.  The editors are pretty gnarly too.  The benefits do include everything except the ability to "blog".
* Static site generators actually do solve the blog and wiki problem, but aren't really mobile friendly for my needs.  Most require a large amount of dependencies.  I really don't want to install `ruby` or `node` just to start developing my website.  Hugo was an exception, written in `go`, meaning it's a static binary with "no dependencies" so-to-speak.  However, the interface is still through a CLI, which makes composing and publishing from a phone difficult.

## The Solution

I actually really liked the idea of using Hugo, writing things in Markdown, and using an alternative interface to run the hugo management commands for me.

The Markdown UX for content creation is pretty nice.  I can program in partials to do more advanced work.  I hope to never need to write raw HTML in my markdown, and instead use the Hugo preprocessor to make some nice APIs for me.  It mostly just means my website will probably have a nice overall consistent style with good semantic tagging.

The content creation UX will need work.  I imagine I will make a small flask app that will run hugo commands under the hood.  The work will require:

* List drafts for editing and publishing
* Create new content as drafts
* Preview drafts before publishing
* Edit or unpublish existing pages
* Authentication to show/hide internal UI

These actions cannot be part of the standard UI because the real content is static.  There's no server to decide when to show the admin options.  Instead, I'll create an admin console to control the pages.

# The Archetecture

I decided to use nginx as the web server because I've always hated Apache, it's confusing and ceremoneous and everything is written in some cryptic magical text.  I found what the most popular web servers are and it's Apache or nginx, so I decided to read the nginx guides which ended up being kind of confusing but the product itself seemed fine.

Beyond that, I'll have a flask web-server that is run with uWSGI based on [this article from Justin Ellingwood from Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04 "How To Serve Flask Applications with uWSGI and Nginx on Ubuntu 14.04").  I'm familiar with flask and it's pretty easy to write, I don't need anything fancy, just a simple hacky admin panel with authentication.

I could configure nginx to serve `/admin` to flask and `/` to the static files using [my new knowledge from Digital Ocean's Justin Ellingwood](https://www.digitalocean.com/community/tutorials/understanding-nginx-server-and-location-block-selection-algorithms "Understanding Nginx Server and Location Block Selection Algorithms").

I would then make `/admin` self-reliant.  It could handle other things like `/admin/url_or_path` or even `/admin?url_argument=foo`.

# The Implementation

So based on the [nginx docs](https://www.nginx.com/resources/wiki/start/index.html), the nginx config will look something like:

```
http {
    server {
        location / {
            root ~/hugo/content/;
        }

        location /admin {
            # not sure yet
        }
    }
}
```

I think being able to list all drafts is nice, but also list all content too.  Hugo has built-in support for listing drafts with `hugo list drafts` but has no ability to list all content.  I think I can replicate this with something like `find content/ -regex ".*md"`.

I can use [python-frontmatter](https://pypi.org/project/python-frontmatter/ "python-frontmatter on pypi") to parse the title, draft status for display.  Additionally, I could parse the files for existing tags so that I can properly tag things easily.  This also means I can build prod without drafts, but still have admin look and edit drafts.

I can configure nginx to serve a preview subdomain to preflight my changes before submitting.

# Known Issues

I don't really have a "revision" solution yet.  I could commit and push so things are tracked in history.  I only really have to do this to the content/ folder under hugo.

I don't really have a "deploy" solution yet.  Pat David suggests in [Atomic Publishing a Static Website](https://patdavid.net/2017/04/atomic-publishing-a-static-website/) that `cp --archive --link` will be compressed and small.  

* **static site**: I could just move the files into the right places.  The static site will work fine.  Must be automatically triggered?
* **uwsgi**: They [list several alternatives](https://uwsgi-docs.readthedocs.io/en/latest/articles/TheArtOfGracefulReloading.html#standard-default-boring-graceful-reload-aka-sighup) but I think boring is the simplest.  Must be manually triggered?
* **nginx** has really good reloading apparently since it's just a config, and the upgrade process exists.  Must be manually triggered?