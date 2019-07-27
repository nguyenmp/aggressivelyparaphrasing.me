---
title: "Hugo's Trailing Slash"
date: 2019-07-27T02:58:28Z
draft: true
---

I found a weird behavior when setting up my personal website.  Whenever I clicked a link on my website to "/portfolio", it would redirect me to the correct host and path, but on port 8080 instead of port 80.

## Context

I'm not exactly sure what was going on honestly but there's some key discoveries.

Although it's undocumented, I strongly believe NearlyFreeSpeech.NET runs an HTTP proxy in front of my own HTTP server.  Their proxy handles SSL termination and HTTP to HTTPS forwarding, which are both pretty convenient.

NearlyFreeSpeech.NET won't let you run as root, so you can't use port 80 when running a custom web server.  Personally, I didn't find a problem with this.  I built Nginx on the machine, then configured it to listen to port 8080, a standard alternative port used by a lot of other software.  Then, I configured NearlyFreeSpeech.NET to forward traffic from their proxy on port 80, to my server running on port 8080.

Finally, I had a link on my header that would point to "/portfolio".

## The Problem

When clicking the "/portfolio" link, I would go from https://aggressivelyparaphrasing.me/ to https://aggressivelyparaphrasing.me:8080/portfolio.  Note the addition of port 8080 to the URL.  This won't work because my web-server on port 8080 is behind NearlyFreeSpeech.NET's proxy running on port 80.

After investigating a bit, I googled "nginx trailing slash redirect port" and found [this stack overflow post](https://serverfault.com/questions/351212/nginx-redirects-to-port-8080-when-accessing-url-without-slash) talking about my problem exactly.  It seems like when Nginx resolves a redirect, it also pushes the port it is listening on in the Location header it sends back to the user.  This makes sense!  If the client is hitting an uncommon port that's not 80, then a redirect might take it off of 8080 and so the redirect should maintain that port.  However, when the client asked for port 80, when Nginx thinks is really port 8080, then we have a problem.  I thought, maybe Nginx should read the Host header and use that instead, unless it doesn't contain the port.  After further investigation, it seems like they have an option called `server_name_in_redirect` which does look at the Host, so I suspect the Host header doesn't contain the port after all.

## The Fix

After experimenting for a while, I gave up temporarily.  I was debugging another issue where my sample page wasn't loading.  I use this sample page to show all the various HTML tags and document structures in one page so that I can judge the look-and-feel of any style changes in one go.  I remembered that Hugo has poor support for optional trailing slashes by default.  In other words, going to "/sample" will fail while going to "/sample/" will succeed.  This is mostly due to the fact that it's a static site.  I kind of wonder if there's a way to support it either from Nginx or in Hugo.  That's when I realized this same problem applies to "/portfolio".  In fact, when I typed in "/sample" by hand, it hung reaching out to port 8080.

In the end, I just changed my link to "/portfolio/" with a trailing slash and everything worked all dandy.

After discovering the root cause and the stack overflow question, I settled on adding support for [ports_in_redirect](http://nginx.org/en/docs/http/ngx_http_core_module.html#port_in_redirect).  Contrary to the stack overflow post, it seems like it's allowed in [server, location, as well as html](http://nginx.org/en/docs/http/ngx_http_core_module.html#port_in_redirect).  Since I wanted this to apply to all my servers on all redirects performed by nginx, I set it in the html block.

You can see [the change](https://github.com/nguyenmp/aggressivelyparaphrasing.me/commit/59a636827c06c8d99e3566463083c64a8b896b30).
