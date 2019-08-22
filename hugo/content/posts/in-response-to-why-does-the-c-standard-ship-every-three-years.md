---
title: "In Response to ‘Why Does the C++ Standard Ship Every Three Years’"
date: 2019-08-18T18:48:58Z
draft: true
---

After reading [the original blog post](https://herbsutter.com/2019/07/13/draft-faq-why-does-the-c-standard-ship-every-three-years/) detailing the explanation, I read [some of the comments on HackerNews](https://news.ycombinator.com/item?id=20428703) and even [the few on Lobsters](https://lobste.rs/s/k0oqi8/why_does_c_standard_ship_every_three_years).  Unfortunately, it felt like a lot of the comments missed the lesson that I took from the FAQ, which centers more on project management rather than a historical account.  To me, the value of this reading was understand how the C++ standards committee arrived to the conclusion that a harsh time-based release cycle was objectively better than the feature-based release cycle.  In this post, I draw from my experience and compare against what Herb Stutter posted.

{{< break >}}
## TODO

I want to emphasize:

* the empirical measures they used
* the comparison of 3 year release cycles to 2 week sprints
* the slip, I see it in my leadership at every level because their reputation is banked on these releases
* the comparison to pull requests containing multiple changes, it’s all or nothing and all the minor QOL improvements are held back by the much larger, riskier, and more debatable change

## Good Job with the  Empirical Data

I really appreciate the use of some objective measures in the post.  It’s convenient that they have 25 years of release and development to draw upon, but I still find it rare to have topics on project management like this that actually talk about the numbers that came out of these types of decisions.

There are two numbers in particular that’s I really enjoy:

First, the calculation of quality per release.  Because you release features and bug fixes as they are finished, 

Second, the calculation of features per year.  They retorted the comparison that they now have two minor 
















