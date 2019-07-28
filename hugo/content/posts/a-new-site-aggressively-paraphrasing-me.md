---
title: "A New Site: Aggressively Paraphrasing Me"
date: 2019-07-28T10:16:44Z
---

Over the past few weeks, I've been working on redesigning and reimplementing my personal website.  Today, I want to talk about my thoughts and actions behind this change.

{{< break >}}

## Motivation

I have been journaling for a bit of time and Google Docs started to fail at around 200 pages.  The page itself was getting slow to load and would sometimes bug out.  It took a long time to jump between different sections of the document.  I had already transitioned to a split "wikis" versus "notes" style but it was difficult to transition between them.  The document itself didn't feel like an archive, even though I wanted it to be one.

Moreover, my hosting provider decided to shut down and I wanted to spend some time working on my site again.

## Requirements

To begin, I thought about what I really wanted out of my journaling system and website.

* **Notes vs Wikis**; I'm pretty excited to try out this idea of separating long running reference pages from instantaneous thoughts.  Unfortunately, most platforms are either blogs or wikis.
* **Mobile friendly**; I want to be able to take notes wherever I am.  An example is a friend suggests a good place to eat while we are walking in the park.  I want to be able to take that and put it into my "foods to eat" reference page.
* **Fast and scalable**; I don't want to have to wait too much on large assets, javascript, external dependencies.  Google Docs takes a surprising amount of time when it starts scaling to the hundreds of pages.  Ideally, I can post endlessly and have dozens reference pages that are dozens of screens long.
* **Sharable**; Often times, I want to be able to share my reference pages to individuals.  Sometimes, it's a new person who wants to get into Anime so I want to share with them my top picks.
* **Searchable**; Sometimes, I have a need to go back and find some piece of information I left buried away somewhere.  Usually, they're in the reference pages, but sometimes they're just a note.  I think I will start having more in notes as I start writing responses to reading pieces.
* **Error resistant**; I'm pretty terrified of losing this data.  I can trust Google to not lose all the material I've been working on, but can I trust myself?  Revision history would be nice.
* **Fine Controls**; I want to be able to control a lot of weird aspects of my website.  After reading the Mozilla guide to web development, there's a lot of minor things I really like, like definition lists, citations to quotes, link titles, and just a very strong ability to finely adjust the design and content of my website, like the CSS, headers, footers, etc.

## Prior Works

Most existing solutions were dissatisfying in some way, due to my desire to have both a "blog" and a "wiki".

* Wix and Square aren't really blogs or wikis.  The contents are pretty static and the tools to build these websites are incredibly heavy, since they're website building tools, rather than content creation tools.
* Blogger and Wordpress aren't really wikis and aren't really designed to have long lived posts/pages that are edited often.  Wordpress seems to have an Android app for posting, but it seems like a WYSIWYG editor.
* Running your own wiki seems pretty sketchy.  A lot of the software is pretty big and looks ugly.  The editors are pretty gnarly too.  The benefits do include everything except the ability to "blog".
* Static site generators actually do solve the blog and wiki problem, but aren't really mobile friendly for my needs.  Most require a large amount of dependencies.  I really don't want to install `ruby` or `node` just to start developing my website.  Hugo was an exception, written in `go`, meaning it's a static binary with "no dependencies" so-to-speak.  However, the interface is still through a CLI, which makes composing and publishing from a phone difficult.

## The Solution

I actually really liked the idea of using Hugo, writing things in Markdown, and using an alternative interface to run the hugo management commands for me.

The Markdown UX for content creation is pretty nice.  I can program in partials to do more advanced work.  I hope to never need to write raw HTML in my markdown, and instead use the Hugo preprocessor to make some nice APIs for me.  It mostly just means my website will probably have a nice overall consistent style with good semantic tagging. something the [Mozilla Web Dev guide](https://developer.mozilla.org/en-US/docs/Learn/HTML) pushes a lot and I appreciate.

The content creation UX will need work.  I imagine I will make a small flask app that will run hugo commands under the hood.  The work will require:

* List drafts for editing and publishing
* Create new content as drafts
* Preview drafts before publishing
* Edit or unpublish existing pages

These actions cannot be part of the standard UI because the real content is static.  There's no server to decide when to show the admin options.  Instead, I'll create an admin console to control the pages.

## The Architecture

I prefer nginx over Apache purely because I find it easier to manage and configure.

I found NearlyFreeSpeech.NET and they were incredibly cheap so I decided to give them a try as a hosting provider.

NearlyFreeSpeech.NET hosts an HTTP proxy on port 80.  They forward the request to my nginx server on port 8080.

Based on the requesting hostname (dev.\_.me, admin.\_.me, \_.me), nginx either reads from the static site file system, or forwards to my flask app.

My flask app (scorsese) does all the management on the dev.\_.me file system and pushes the changes to GitHub.  It then redeploys \_.me (prod) from GitHub so prod is always clean.

You can find the technical details and implementation on the [README.md of the GitHub](https://github.com/nguyenmp/aggressivelyparaphrasing.me).

## Security

One thing that scared me was implementing my own solution, posting the source, describing it in detail, and having someone try to attack it.

Because of this, I decided to do a couple of things:

* Protect against XSS.  I sanitize inputs that go to the file system, I render everything using jinja.
* Protect against Clickjacking.  I configured nginx to disable iframe embedding using some headers.
* Protect against CSRF.  I implemented a CSRF token system for all POSTs.
* Protect against everything.  dev.\_.me and admin.\_.me are both behind an nginx Basic Auth directive.

The world is a scary place and this website is putting myself out there.  I'm not claiming my website is secure, just that I'm thinking about it.
