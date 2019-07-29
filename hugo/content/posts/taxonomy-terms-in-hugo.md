---
title: "Taxonomy Terms in Hugo"
date: 2019-07-29T06:43:12Z
draft: true
---

I've been trying to get "tags" working in my Hugo based "aggressivelyparaphrasing.me" website for a day now and it's a nightmare.  I'm going to talk about how things don't behave as expected and how I dealt with them.

{{< break >}}
## Taxonomy and Taxonomy Terms

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