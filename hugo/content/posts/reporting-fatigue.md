---
title: "Reporting Fatigue"
date: 2019-11-03T21:01:22Z
draft: true
---

I was browsing [a lobste.rs post](https://lobste.rs/s/jcxz0w/they_might_never_tell_you_it_s_broken) which pointed to [a blog post called ](https://pointersgonewild.com/2019/11/02/they-might-never-tell-you-its-broken/).

There are several reasons I stopped filing as many bugs:

1. There are too many to file and many often don’t get worked on.
2. It’s often not worth filing a bug.
* In the modern software market, a lot of software is a commodity.  For example, style checkers in python is something I looked into recently.  I tried the one that was suggested by the google style guide, but after spending 10 minutes having difficulty getting it running, I decided to use black instead which worked out of the box.
* Filing a bug is a guaranteed loss of time.  I encourage people to file good bugs and I try to explicitly reward well written bugs when I receive them, usually with a direct and personalized thank you note stating the specific sections I found most useful.  However, when I file bugs to other people, often it feels like they didn’t even read it.  Perhaps it a communication issue or fatigue from reading and triaging so many reports, but it conversely fatigues me from filing bugs.
* It often doesn’t help.  The chances of it getting looked at within a month is probably 50% and the chances of it getting fixed without specifically escalating it to individuals is even lower.  Often times, I’ll try and contribute very simple documentation changes to fix minor typos and those take months to get looked at and fixed.  I used to file bugs for an app I used every day to help improve it.  Eventually, after years of not using it, I got over a hundred emails saying my reports have been closed because the code has changed so much since I file the bugs that they’re not actionable anymore.
* Making bugs actionable is hard.  There’s lots of little things that can help make a bug actionable from the get-go.  The ability to run the integration tests in the clients environment can give signals to faulty assumptions.  A template for various basic information is also useful for forcing clients to provide commonly required configuration and context.  A unified logging story that the customer can just provide the developers with all the debugging information they need.  It’s a pain to have to activate debug logging as well as copy files from a dozen different places and run a bunch of dumping commands that are all mostly undocumented or difficult to follow.  I encourage a simple “debug” tool that dumps everything a dev would need, and make it the developers responsibility to update that tool whenever a bug is not actionable.

{{< break >}}
## Second Header
