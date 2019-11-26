---
title: "Boomerang and Analyzing Contribution Sizes in Tarballs"
date: 2019-07-30T01:30:47Z
draft: true
tags:
- debugging
- statistics
---

About a year ago, I had participated in the pilot cohort of a new program at Apple called "boomerang."  For about 3 months, I went from my current team writing automation tools to my foster-team working on the logging and diagnostics framework.  I wanted to share a bit about my experience being a boomerang as well as the problem I worked on.

{{< break >}}

## A Bit About Boomerang

Apple implemented a new rotation program that allows individuals to switch to another team for about 3 months.

I was fortunate enough to be in the pilot cohort!  Normally, I'd be working on automation tools and infrastructure but I was accepted as a temporary "boomerang" onto the diagnostics team.  In my standard day-to-day, I work with python and Javascript to write tools for automation teams at Apple.  Hopefully, my tools enable people to automate.  My time on the boomerang team was primary writing in C, with some Swift and Objective-C in some cases as different projects came up and required those skillsets.

I chose to boomerang for several reasons 


## The Big Problem With Sysdiagnose

To understand what makes the sysdiagnose so big, we have to understand what it is in the first place.  At a high level, it's a tarball of a lot of different logs.  Most are simple text files such as samples and the logs for the sysdiagnose itself.  Some are binary files such as those of the packet dumps.  However, there is a specific special case called the systemlogs.logarchive which I like to call the larchive, though that never seemed to really catch on.

The larchive is a special format of logs that congregate all the the various calls to the logging framework on all the different platforms.  It offers some awesome features like automatically rolling over logs, defining different tiers of logs for different retention policies.  For example, you might only have a megabyte allocated to your debug channel, but that channel might produce a megabyte a minute.  The logging system will automatically keep an in-memory data store of your logs and only write it out to disk if something triggers a log dump.  This helps keep things fast and efficient as you avoid doing unnecessary IO until it's needed.  This also means that the larchive is represented a bit differently than logs that traditionally get shuffled from standard output. 

## Understanding What Makes Logs Big; Understanding GZIP and DEFLATE

So a sysdiagnose is a huge tarball 

## Better and Worse Estimates

So an accurate measure is actually by definition pretty complicated.

A single file doesn't add a definite amount of data to the tarball because the ordering of files, the shared content between files, and the file sizes all contribute to this multi-variate problem.  For example, the first crash log could easily be 32kb, but if the target process is in a crash loop, constantly crashing over and over again in the same stack trace, then the file will actually grow only in a few bytes in size for each new file.  This is because the sliding window of back references still covers the entirety of the file and the contents of the crashlog will be almost identical each time.

In the end, measuring the exact size was too difficult to calculate and really was digging at the problem at too low of a level.  To really understand what we want, let's take a step back.  We originally proposed this project because there were logs that were hundreds of megabytes in size, approaching gigabytes in some cases.  This is well beyond what the compression window can support since it's only 32KB in size based on the definition of the DEFLATE algorithm.  Any notion that the compression between files is really making an impact to the overall file size is misguided.  If files are redundant, they will be compressed, otherwise they will blow up the file.  In the end, there are only hundreds of files that could contribute to the gigabyte tarball.  What we really are looking for is files that basically cannot be compressed or are humongous even when compressed.  We are looking for files that add hundreds of megabytes when we add them to the log archive.

Once we accept that we are looking at a granularity of megabytes rather than bytes, we had one interesting idea: stat the file every time we add new content to the archive.  This was interesting for two reasons: (1) we didn't really need to add much instrumentation to the code to understand how the compression was actually performing (i.e. we don't need to know the compression ratios or how much overlap there was between files) and (2) we could only get granularity of about 4kb which isn't great at a low level, but is perfectly fine at the grand scale of megabytes.  That is to say, when we add a file, if it doesn't force a flush at the 4kb block, then we will consider it to have added zero bytes to the archive.  This is weird logically, but doesn't really matter in the end of the day since the difference between 3kb and 0kb is nothing compared to 1mb.

## flamegraph

Once we could measure how much each file contributed, we still needed a way to visualize the data.  A sysdiagnose isn't just an archive of files, it's really an archive of folders containing files.  Some folders like "bluetooth" make a lot of sense to look at in a high level, while others like the "Logs" folder don't really make sense unless you look at the individual contributors.  Sometimes, a folder like "system logs" will have a lot of content but only because it has thousands of contributors, each only a dozens or hundreds of kilobytes in size.

This type of problem has been addressed by file-size visualizers in dozens of apps.  OmniDiskSweeper, for example, shows a folder explorer that interactively drills down into each folder as you click.  This is fine but not really useful in our case if we want to present the data.  Another way is to use a Sunburst diagram (or hierarchical pie chart).  While the visualization fits really well, the tools were really hard to figure out and use.  In the end, the easiest way to visualize this was to use a flamegraph which has code publicly available that is incredibly easy to interface with and outputs an interactive SVG.

## The Results

[INSERT PHOTO HERE]

So in the end, we actually have two ways to look at this: one is to look at the logs and see how many kilobytes each file path adds to the total archive, and the other is to look at a visual to show hot spots in space allocation.  What is interesting to me is that while the visualization is cool and actually really easy to internalize to find suspicious zones, it's also really bad at showing aggregate data.  It's really hard to visualize that a file is usually very small but sometimes blows up the archive.  This is far easier to show in just metrics around the individual data.

This code is available in the OS and you can totally see this if you trigger a sysdiagnose on a mac: `sudo sysdiagonse`.  Once it drops an archive, open it up look at `summaries/diagnostic_summary.log` in a text editor.  You will find stuff like:

```
File: /ASPSnapshots/asptool_snapshot_timesensitive.log -- size: 22381 -- compressed: 0
File: /logs/tailspindb/UUIDToBinaryLocations -- size: 38175 -- compressed: 0
File: /logs/CoreLocation/cache.plist -- size: 6795 -- compressed: 0
```

The compressed section is the delta in the stat of the archive after adding the given content.