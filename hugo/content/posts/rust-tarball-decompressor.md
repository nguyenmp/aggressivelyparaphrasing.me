---
title: "Rust Tarball Decompressor"
date: 2019-07-28T07:48:44Z
draft: true
tags:
- rust
- debugging
---

A few months ago, I wrote a tarball decompressor in Rust.  I needed a tarball decompressor implementation because of some work I was doing, but I decided to have a lot of fun with this.  The actual work was a three line change but this project was incredibly fun.  I decided to try and implement a decompressor entirely out of the specifications for the algorithms, using a language I had never used before called rust.

## Comparing to reference implementations

At this point, I had struggled with the specification for long enough to realize I wasn’t making headway and I needed a different approach.  I decided to look at another reference implementation to see if I could find discrepancies.  If I could find the byte where I start drifting, then I could potentially find the error in logic.

### infgen 

The first reimplementation I found was infgen.  It prints out a bunch of internal debug information about various archive formats.  Unfortunately, the information didn’t help me as it was too high level.  I also couldn’t modify the code because it’s one file containing 1400 lines of C.  I added a few print statements here and there but I couldn’t really figure out where to start with adding more logging.  I think part of the problem is that it’s an incredibly feature rich program, supporting many archive formats and commands.

### Simple DEFLATE decompressor

I eventually found some random project that describes itself as a “clear implementation of an inflated for the DEFLATE compression format.”  I chose this because I highly suspected my bit-twiddling logic to be faulty.  Tar is an incredibly simple format.  Gzip, and DEFLATE backing it, are incredibly intricate.  

Also the code is in Java with the largest file being around 300 lines long.  I felt very comfortable here.

This tool also didn’t output, much like infgen, but I quickly found some locations to just start printing output bytes so I could compare.  I decompressed the same file between my project and theirs and started searching for when the output stream diverges.  I set a breakpoint to trigger when we hit the specific byte sequence.  It was here that I found the byte that went wrong.

## The Bug

After all the debugging and hair pulling, I finally found that I was doing a double-write when we encounter an end block in DEFLATE.  You can find my fork with it’s debugging changes.

## The Result

It works!  It decompressed most content readily and quickly.  It’s not fully implementing the specification so it won’t work with all files but it’s usable.  However, it did not handle my 200MB tarballs very well and hung for some indefinite amount of time.  I didn’t do the math on how long it would take but I suspect it might just be hung.  I decided that was enough fun for the week and hung up the project.  You can find the code at GitHub.