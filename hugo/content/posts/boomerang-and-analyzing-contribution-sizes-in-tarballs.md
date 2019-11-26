---
title: "Boomerang and Analyzing Contribution Sizes in Tarballs"
date: 2019-07-30T01:30:47Z
draft: true
tags:
- debugging
- statistics
---

About a year ago, I had participated in the pilot cohort of a new program at Apple called "boomerang."  
Apple implemented a new rotation program that allows individuals to switch to another team for about 3 months, and I was fortunate enough to be in the pilot cohort!  Normally, I'd be working on automation tools and infrastructure but I was accepted as a temporary "boomerang" onto the diagnostics team.

{{< break >}}
## A Bit About Boomerang

## The Sysdiagnose

To understand what makes the sysdiagnose so big, we have to understand what it is in the first place.  At a high level, it's a tarball of a lot of different logs.  Most are simple text files such as samples and the logs for the sysdiagnose itself.  Some are binary files such as those of the packet dumps.  However, there is a specific special case called the systemlogs.logarchive which I like to call the larchive, though that never seemed to really catch on.

The larchive is a special format of logs that congregate all the the various calls to the logging framework on all the different platforms.  It offers some awesome features like automatically rolling over logs, defining different tiers of logs for different retention policies.  For example, you might only have a megabyte allocated to your debug channel, but that channel might produce a megabyte a minute.  The logging system will automatically keep an in-memory data store of your logs and only write it out to disk if something triggers a log dump.  This helps keep things fast and efficient as you avoid doing unnecessary IO until it's needed.  This also means that the larchive is represented a bit differently than logs that traditionally get shuffled from standard output. 

## Understanding What Makes Logs Big; Understanding GZIP and DEFLATE

So a sysdiagnose is a huge tarball 

## Better and Worse Estimates

So an accurate measure is actually by definition pretty complicated.

A single file doesn't add a definite amount of data to the tarball because the ordering of files, the shared content between files, and the file sizes all contribute to this multi-variate problem.  For example, the first crash log could easily be 32kb, but if the target process is in a crash loop, constantly crashing over and over again in the same stack trace, then the file will actually grow only in a few bytes in size for each new file.  This is because the sliding window of back references still covers the entirety of the file and the contents of the crashlog will be almost identical each time.

The 

There are a couple of ways we could approach figuring out how the file grows 

## flamegraph

