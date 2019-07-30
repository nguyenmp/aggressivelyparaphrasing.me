---
title: "Taxonomy Terms in Hugo"
date: 2019-07-29T06:43:12Z
draft: true
tags:
- meta
- hugo
- debugging
---

I've been trying to get "tags" working in my Hugo based "aggressivelyparaphrasing.me" website for a day now and it's a nightmare.  I'm going to talk about how things don't behave as expected and how I dealt with them.

{{< break >}}

## What I Want

I wanted a way to annotate my blog posts with topics.  Some overlap, some don’t.  For example, I wanted one generic programming tag with a bunch of specific languages tag for python or rust.  I also wanted ones for web development.  The goal was less for the reader and more for myself to see what to write about, which the reader could see too, but I find that less useful.

There are four user facing changes I expect:

* the header will now contain a list of topics I write about
* the posts will contain a list of topics it’s tagged with
* a user can click a topic to view other posts for that topic (/tags/programming/)
* a user can see a list of all topics (/tags/)

## Taxonomy and Taxonomy Terms

Hugo ships with a feature called taxonomies.  This feature is for categorizing content using keys and values or arrays of values.  By default, “category” and “tags” are automatically set up.  All you have to do is add them to the front matter of your document and you’re all set.

## Going beyond defaults

Realistically, what will be rendered for /tags/ and /tags/programming/ will be your list.html template or your single.html template.  This is what is shipped in most themes by default, as far as I can tell, after downloading a handful and looking at the source.  This means that the content of these pages aren’t particularly interesting or tailored.  I wanted some specific features:

* when looking at a particular tag, I wanted a description of what the tag means.  When I say languages, is that human languages like Japanese and Chinese, or computer languages like rust and go.
* when looking at a list of tags either in the tag index (/tags/) or in the header or footer, I want to see a count of articles tagged with that tag
* when looking at a list of tags, I want it sorted by usage in the header

By default, lists are sorted by date.  Default list.html templates don’t know about descriptions or how to represent them, mostly cause there isn’t one and it’s theme dependent.  I don’t use descriptions for my posts so I never built that in.  Moreover, the way I render posts and tags are different.  With posts, I want to show the publishing date and title; but with tags, I want to show the title, count, and description.

## list.html vs single.html

## tags vs categories

## taxonomy.html

## Non-deterministic layout selection

I noticed that sometimes, after I edit a page and the page reloads with live-reload, the page changes which layout it selected.  This is most-assuredly a bug because often, the content I'm changing is just a string that already existed in some description or body somewhere.

```
rm -rf public/ && hugo -D --enableGitInfo --noHTTPCache --path-warnings --renderToDisk --watch=false --disableLiveReload --disablastRender server
```

## Adding _index.html fixed the top level page

## Adding _index.html fixed the leaf level pages

## Looking Back, Why Was This Hard?

I noticed that the Hugo docs had a section called  “Examples: Layout Lookup for Taxonomy Terms Pages“ that defined two sections:
* Taxonomy terms in categories
* Taxonomy term in categories

My thought was, there must be a difference between a taxonomy term and taxonomy terms.  The plural “terms” must be for the list page, equal to list.html whereas the singular “term” must be equal to the single.html.  I’m pretty sure that this is really just a typo.  The real difference between the rows is the first row is for XML responses and the second row is for HTML.  Both rows are to show what posts fall under a specified taxonomy.

There is an entirely separate section above that that says “Taxonomy list in categories”, whatever that means.  In retrospect, it’s clear to me now that, given the section named “Examples: Layout Lookup for Taxonomy List Pages”, this is the “list.html” page for taxonomies.  But it’s unclear if this is:

* the list of taxonomies like “category” and “tags”
* the list of values for a given taxonomy like “action” or “mystery” for the “genre” category
* or if it’s the list of pages assigned to the given taxonomy

The only other piece of documentation was the section titled “Taxonomy List Templates” and Taxonomy Term Templates” under the “Taxonomy Templates” page.  While the titles seem promising to include examples and clear documentation, they’re incredibly terse, linking only to the previous template lookup order documentation with no examples provided.

## My Suggestion

I don’t want to just complain, after getting something working, I want to help make things better.  I also don’t expect things to be perfect, especially given the latest version is 0.55.6, hinting at its immaturity.