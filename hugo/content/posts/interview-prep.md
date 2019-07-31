---
title: "Interview Prep"
date: 2019-07-30T04:42:34Z
draft: true
---

I decided to start looking for a job and decided to document my process.  Part of the motivation is to organize my own work.  Another is to help critically think about the process and decisions through writing.

{{< break >}}
## Primers

These are short but valuable write ups about interviewing in tech.

### 10 Offers, 100 Days. The Journey by Stepan Parunashvili

The [blog post](https://m.stopa.io/10-offers-100-days-the-journey-16a0407b8d95) goes over this individual’s adventure of being highly successful at winning offers at some pretty competitive companies,

There are a few high level points that are pretty valuable:

* Communication with your support group is pretty interesting, some have been pursuing my goals for longer than I have
* At some point, the interview is less focused on algorithms and more on high level systems and project design and soft skills.  Higher level positions are about leading people and projects.  Often, questions about failures, conflicts, failures, deadlines, and weaknesses are to point out and expose experiences dealing with these types of responsibilities.
* Leadership usually entails bringing people up to speed, so it might be worth emphasizing on my resume.  Previously, it was mostly technical focus and project focus, rather than people focused.
* They recommend reading Elements of Programming Interview
* I should formalize my reasons for searching for a new job.  A strong, positive motivation can help establish “strong-fits” for people to recommend you to, and make you more desirable for those companies.
* It may be valuable to “figure out my level” and also to figure out the compensation ranges for that level, using [levels.fyi](https://levels.fyi)
* There is a structure to system design questions.  This is repeated in a lot of other blogs.

Below are some quotes I pulled out for reference and to reflect upon.

> Sit down and reflect: What got you here? What did you love about your last job? What would the most amazing opportunity look like?

 I need to do this.

> A week or so after you’re into the book, schedule practice interviews. My favorites are https://interviewing.io and https://pramp.com.

Might be worth trying since they can do system design interviews.

> For System Design, I also suggest three steps. First, master the structure — scope down, go broad, outline a complete solution, go deep on as many components as you can, then go the extra mile, to share how you would actually launch the system. The “System Design” module in the course does a great job of going deep on this. Next, as you go through the practice interviews, you’ll start to notice places where you can improve. Start noting those down and build a plan to learn. For example, if you don’t know how to scale, you can search “{Company Name} InfoQ” and find some awesome talks. If you’re unsure about concurrency, the book 7 concurrency models in 7 weeks can ramp you up. Don’t know much about databases? 7 databases in 7 weeks.

I fear the system design section.  I don’t have much practice in this compared to LeetCode for algorithms and data structures.

> The purpose of the Experience Interview is to understand your scope — the kinds of problems you can solve — and whether you are a culture fit. This interview type largely takes care of itself if you’ve centered on your narrative (you know what you want and where you’re going), and your communication (you know what level you are). The first coneys your culture fit, and the second your scope. You can go deeper on this in the “Experience Interview” module in the course.

I also don’t have much practice answering questions involving soft skills and experience.  I need to figure out these solutions.

> Communicate your level and your narrative. Keep signal and scope top of mind, and communicate clearly during every phase — recruiter screens, technical screens, and and onsites. We go deeper on this in the “Interview Phases” module of the course.

I actually think I don’t do this at all right now.  Part of it was I’ve never really know what I want to do because I’m so open to many options and I like just exploring and trying new things.  When people ask me to tell them what I want, I find it incredibly difficult to express.  However, I also do a pretty bad job expressing what I currently do already.

I think overall, I like how they break down senior engineer interviews, but the actual actionable data is pretty lacking for the two sections I care about the most.  How does one improve on systems questions and experience interviews?  The only real suggestion is read Elements or Programming Interviews, which I’ve seen recommended a lot over the years, but that’s focused on algorithms and data structures.  It does suggest that the real content is in [jobsearch.dev](https://jobsearch.dev/) which is free so maybe I’ll try it.

### Software Engineering Paths by Anthony Sarkis

[This blog post](https://medium.com/@anthony_sarkis/software-engineering-paths-180595fd229c) is mostly speculation about how people perceive experience and job requirements.  It suggests skills aren’t a binary yes or no, nor are they really a spectrum of endless non-discrete markers.  This article suggests they’re trinary.  That you’re either lightly experienced, moderately experienced, or an expert.  Moreover, these levels are skill and topic dependent, you are not just an expert, you are an expert in some topic or field.

The article is less about how to succeed in the interview, and more helpful for understanding how the interview process is seen by some people behind the table.  It’s also helpful for reflecting on my own expertise and skills.  I hunk categorizing ones skills this way is super helpful in knowing expertise.

Overall, this is more of a fun read than a serious one for my particular goals here.

### Peak: Secrets from the New Science of Expertise

[This book](https://en.m.wikipedia.org/wiki/Peak:_Secrets_from_the_New_Science_of_Expertise) talks about how the best way to improve is to just do things for a very long amount of time, but also that the doing must be deliberate practice, it must be work just outside your comfort zone.  Otherwise, you just stagnate at your level.  I haven’t read it yet but I’ve read and heard a lot about it.

[There’s an excerpt on Salon](https://www.salon.com/2016/04/10/malcolm_gladwell_got_us_wrong_our_research_was_key_to_the_10000_hour_rule_but_heres_what_got_oversimplified/) that’s probably good enough as a primer.  I also haven’t read this yet.

When I think of those ideas of deliberate practice, I think about the following sections, that I’ve practiced algorithms significantly over the last five to six years, but have very little practice and experience around system design questions and experience questions.  It’s also clear those are required to getting to the next level.  As such, I’ll spend most of my time on the latter, since that’s where I need the most growth.

## Algorithms

For the most part, I feel like I have the basics down and there’s established systems of studying for this type of interview.  In particular, I feel like this category is much like the SAT, where you can learn how to answer these types of questions, rather than any particular innate talent.  Moreover, like the SAT, practice really does significantly improve performance.

### LeetCode

Honestly, I much prefer LeetCode over HackerRank, if purely for the ergonomics of answering questions.  HackerRank deals with standard input and standard output, whereas LeetCode is mostly called functions, acting much more like unit-tests so you real with the meat of the algorithm instead of the ceremony of parsing and printing.

### Cracking the Coding Interview

I read this once in college before landing my first job.  I think it’s an okay introduction but lacks hard questions.  I intend to reread it with the latest edition.

### Elements of Programming Interview

This book is often recommended but I’ve never read it.

## System Design

This is kind of the “next level” technical interview question.  Im rather disappointed by the lack of prep material available in this space, mostly because actual experience for these things can be hard to come by.  In particular, I don’t work on high scale systems very much, though I do understand them and manage a few low scale systems myself.  Because of this, I feel like I need to learn significantly more.

### Pramp

https://blog.pramp.com/how-to-succeed-in-a-system-design-interview-27b35de0df26

The page itself has a helpful step by step guide to approach system design questions.

Additionally, there is a lot of content on that page near the end.

### Grokking the System Design Interview

[Link](https://www.educative.io/collection/5668639101419520/5649050225344512)

It’s $80, but that’s a small price to pay for my future.  I just balance the cost against the potential future benefits of salaries, career growth, and happiness.

### Recommendations from Stepan

> For example, if you don’t know how to scale, you can search “{Company Name} InfoQ” and find some awesome talks. If you’re unsure about concurrency, the book 7 concurrency models in 7 weeks can ramp you up. Don’t know much about databases? 7 databases in 7 weeks.
> 
> https://m.stopa.io/10-offers-100-days-the-journey-16a0407b8d95

https://jobsearch.dev/

### Anatomy of a System Design Interview

https://hackernoon.com/anatomy-of-a-system-design-interview-4cb57d75a53f

They have yet another breakdown, but also more study material to go through.

## Experience, Leadership, Soft Skills

I kind of group up all the soft skills and leadership skills together under “experience”.  I think project management can also fit under here.  Part of the reason is because, in an interview, all of these requirements are checked off together.  People ask about your history leading projects, dealing with conflict, missing deadlines, all to probe at these non-technical skills.  I felt like I was lacking here so I decided to read A LOT about it.  It’s also rather fortunate that there’s a significant amount written on these topics.

### Pragmatic Programmer
### Culture Code: The Secrets of Highly Successful Groups
### The Mythical Man-Month
### Soft Skills: The Software Developers Life Manual
### Peopleware: Productive Projects and Teams
### The Manager’s Path: A Guide for Tech Leaders Navigating Growth and Change

I originally got this tech management book half a year before I started my job search.  I felt my ability to connect and communicate with my leadership had gotten rusty and I wanted to learn what it was like from their point of view.

My biggest take-aways are:

* one-on-ones are incredibly important, always maintain an open channel of communication
* rants and venting sessions are fun but not productive
* I need to recap the team lead content
* managers and leaders are not mind readers
* publicly praise, privately criticize

## Negotiation

### How I negotiated a $300,000 job offer in Silicon Valley

[This blog post](https://blog.usejournal.com/how-i-negotiated-a-software-engineer-offer-in-silicon-valley-f11590f5c656) is actually a sequel to one titled [“I interviewed at six top companies in Silicon Valley in six days, and stumbled into six job offers”](https://blog.usejournal.com/i-interviewed-at-six-top-companies-in-silicon-valley-in-six-days-and-stumbled-into-six-job-offers-fe9cc7bbc996).

Big take away is multiple offers is best, and a good alternative is to be employed.

> **Recruiter**: So, what do you think?
>
> **You**: That’s an interesting offer. I think it’s probably in the ballpark, but it’s not something I’m going to sign right now. I’m going to wait until I hear back from the other places I’m speaking to.
>
> In the above, you let your recruiter know that they’re “in the running”, but that it’s not enough to blow you away. You’re respectful but firm. This is the blueprint for how your discussions should go.

This helps address the initial offer.

> My initial counter-offers sounded something like this (I made up the numbers here and provide a few examples):

> **Bar, Inc.**: We were thinking of offering a base salary of around $120,000 with a four-year RSU package of $150,000 and a signing bonus of $10,000. What do you think of that?

> **Me**: How flexible is Bar, Inc. on equity? I’m really looking to stay and grow at a company, and equity is something I really interested in wherever I go. I’m comfortable with something in the neighborhood of $120,000 on base, but I’d definitely like to sign an offer with a larger equity package.

> **FooCorp**: We were thinking of offering a base salary of around $100,000 with a four-year RSU package of $150,000 and a signing bonus of $10,000. What do you think of that?

> **Me**: I think the base is a little bit lower than what I’d like based on my offer from Bar, Inc. for $120,000, and base salary is really important to me. As for the equity package, I was looking for something closer to $200,000. The signing bonus is around what I was looking for.

> There’s a lot of actionable information above for a recruiter without you giving any implicit commitment to any number. FooCorp knows they need to get to $120,000 to meet your other offer. Bar knows that equity is important to you, and equity is something that companies tend to move a lot more willingly. You now have two companies moving in tandem to get a better offer to you and neither of them is talking to each other. This is pretty much how you want this entire process to go.

This helps address the initial counter offers.

> It makes sense to change an established range once another company ups the ante. This is how that discussion went for me:

> **Me**: Hey, I finally heard back from Baz LLC. Their offer came in a lot higher than I was expecting. They offered $150,000 in base, $200,000 in stock, and $40,000 in signing. That being said I think the work FooCorp aligns more closely with my interests, so I’d really like to make something work with you guys. Can we do what we can to get to those numbers? I’d love to figure this out.

> **FooCorp**: Wow, that’s a good offer. Keep in mind FooCorp is {making the world a better place / has amazing potential / is better for your career} and I would hope you wouldn’t be deciding based on a paycheck. I don’t know if we can match that offer exactly, but I’ll see what we can do.

> I went through the above sample conversations so many times and they all went pretty similarly.  They always sounded very doubtful about moving their numbers. They always said it was more than they would typically give up.  They always explained why their company’s mission and culture made up for the difference in comp.  But almost always, they upped the package.  Sometimes they’ll match it. Sometimes they won’t. Sometimes they’ll come close enough that you’ll pull the trigger because it’s such an exciting opportunity. You should always give it a shot, though.

This helps address the final standing offer, like a “last-call” in terms of what people can offer.

Honestly, the blog post is full of examples so it’s worth reading just to appreciate and dissect.  These types of skills I personally feel I lack.

### I interviewed at six top companies in Silicon Valley in six days, and stumbled into six job offers

[This post](https://blog.usejournal.com/i-interviewed-at-six-top-companies-in-silicon-valley-in-six-days-and-stumbled-into-six-job-offers-fe9cc7bbc996) is the original to the above $300k post.  I placed it after because I personally am looking at a higher level position rather than just getting a bunch of offers at big companies since I’m already there.  However, I left it here because I think it’s worth reading.

### Salary Negotiation: Make More Money, Be More Valued by Patrick McKenzie (patio11)

[This long blog post](https://www.kalzumeus.com/2012/01/23/salary-negotiation/) was one I read a long time about and frames the company side of negotiating differently than cost minimization and value maximization.  Honestly, it’s a really fresh perspective for me and I think it’s an often lightly described idea in other pieces.  It’s one of the few pieces that talks about what the other side wants, and how to work with that.  This was recommended from the $300k post as well as the 10 offers in 3 months post.  I read this long before either of those and can say it’s worth the read.  For this goal, I will reread and reanalyze.

### The Business by Rands

I’ve never read [this piece](http://randsinrepose.com/archives/the-business/) but it was recommended by the 10 offers author in that piece.

### Getting to Yes

### Never Split the Difference

## Practicing

There should have been practicing this whole time during preparation, but there’s something special about going through a series of full end-to-end interviews.  Specifically, having another person question you and give you feedback.  Thus, this section is dedicated towards getting real feedback.

### https://interviewing.io/

### https://pramp.com/

### jobsearch.dev

Should probably go under primer or something...

















 