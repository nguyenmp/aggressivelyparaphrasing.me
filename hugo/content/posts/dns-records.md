---
title: "DNS Records"
date: 2019-07-22T16:22:08-07:00
draft: true
tags:
- meta
---

In setting up aggressivelyparaphrasing.me, I really struggled with how to manage domains.

Roughly, there are three main types of DNS records:

1. A/AAAA Records: These map a domain name to an IP Address.  A Records map to IPv4 addresses while AAAA records map to IPv6 addresses.
2. CNAME/ALIAS: These map one domain name to another.  CNAME responds to all DNS queries.  ALIAS responds to only those configured.  This means an ALIAS can co-exist with other types of records on the same name.  Moreover, ALIAS is resolved on the DNS server side, whereas CNAME is resolved client side.
3. URL Redirects: This seem like it's not at hte DNS level but at the HTTP level?
4. MX/MXE Records: These are for mail resolution, where MX points to a hostname and MXE points to an IP address.

Since NearlyFreeSpeech.net only provides a domain name, I must set up my CNAME/ALIAS for my website to point to their domain.

Resources:
https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-choosing-alias-non-alias.html
https://support.dnsimple.com/articles/differences-a-cname-records/
https://www.nearlyfreespeech.net/about/faq#Static
https://support.dnsimple.com/articles/differences-between-a-cname-alias-url/
https://www.namecheap.com/support/knowledgebase/article.aspx/579/2237/which-record-type-option-should-i-choose-for-the-information-im-about-to-enter