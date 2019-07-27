This documents the current setup and codebase backing aggressivelyparaphrasing.me.  It roughly covers the source-code layout, how to run it, and how the different sections integrate.  This documentation is very technical and dives deep into the implementation details.

For a more philosophical analysis, see the homepage of this website.  That document talks about the original problem, the requirements, existing solutions, and my ideal workflow. 

# Project Components

There's four main components for this deployment, which reflects the subdirectories in this repository:

* **the static site** that generates the main html stuff for this website: hugo
* **the editor** that creates a web interface for editing the static content: scorsese
* **the web server** that runs the editor and serves the contents of the static site or the flask app: nginx
* **the python gateway** that allows nginx and the python app to communicate: uWSGI

## Hugo - The Static Site

The hugo section is basically markdown, html, and CSS.  I either edit them at my desk or use the web interface, which edits them for me.

---

At this point in the docs, this is how I created the hugo portion, and my understanding of how hugo works.

```
$ hugo new site hugo/
$ cd hugo/
$ hugo new theme aggpara
$ echo 'theme = "aggpara"' >> config.toml
```

Then I read through the [homepage content generation article](https://gohugo.io/templates/homepage/).  This means create the `themes/aggpara/layouts/index.html` from that documentation as is.

Then I created content for the homepage with: `hugo new _index.md`

For my personal sanity, I finally understood:
* It's a good idea to just create your own theme.  This allows you to separate your "content" from your "presentation"
* You can always add a theme under your theme
* The theme generation gives you nice starting defaults.
* baseof.html contains the generic layout (head, header, body, footer)
* head.html is the `<head>` content for metadata stuff
* header.html appears above all pages
* footer.html is below
* index.html "defines main" for baseof.html to fill the content with

Honestly, I felt like I never really learned HTML deeply until I read [Mozilla's guide](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML).  It's very thorough.  I chose this because there was an article on Lobste.rs that mentioned people should just learn all 150 tags in HTML, they're not that many and they provide a lot of useful built-in features from the browser.

While going through the mozilla tutorial, I felt like I needed a sample.md file to visually see how I would style all my content, from one page.  That way, I can pick the overall style of my site without having to view all my individual pages to see how it all fits together.

## Scorsese - The Editor UI

I implemented a simple flask app that will edit my static site for me using a web interface.  This allows me to make posts and edits on my phone while I'm just thinking about things.  Realistically, I mostly make drafts when thoughts initally come out.  Then I go back and edit my drafts until I'm ready to publish.

## Nginx - The HTTP Server

This handles the HTTP requests initially and determines how it should be served (python or static content).

---

I'm now documenting my steps towards installing nginx.  I'm basically just following their [official guide](http://nginx.org/en/docs/beginners_guide.html "Beginner’s Guide").

I considered installing docker but it's 500+ MB large.  I already had brew installed so I decided to use that instead.

```
Docroot is: /usr/local/var/www

The default port has been set in /usr/local/etc/nginx/nginx.conf to 8080 so that
nginx can run without sudo.

nginx will load all files in /usr/local/etc/nginx/servers/.

To have launchd start nginx now and restart at login:
  brew services start nginx
Or, if you don't want/need a background service you can just run:
  nginx
```

> The way nginx and its modules work is determined in the configuration file. By default, the configuration file is named nginx.conf and placed in the directory /usr/local/nginx/conf, /etc/nginx, or /usr/local/etc/nginx.

I think what I will do is add the default nginx config to version control.  Then, simlink the one on the system to the one in version control.

> Changes made in the configuration file will not be applied until the command to reload configuration is sent to nginx or it is restarted. To reload configuration, execute:
> ```
> nginx -s reload
> ```

I eventually settled with a minimal config that would just render my hugo site on localhost:8080 properly.

```
events {
    worker_connections  1024;
}

http {
    server {
        listen       8080;
        server_name  localhost;

        include mime.types;

        location / {
            root   /Users/marknguyen/MyRepositories/aggressivelyparaphrasing/hugo/public;
            index  index.html;
        }

    }
}
```


## uWSGI - The Python Gateway

My primitive understanding of this is that nginx will receive an HTTP request, and determine if it needs to go to a a python app based on the rules given to it, then gives it to uWSGI to manage the python stuff.

---

I started wtih following their [official getting started guide](https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html).

```
pip install uwsgi
```

Then running is just a matter of:
```
uwsgi --socket 127.0.0.1:3031 --wsgi scorsese --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191
```

# Content

There are two main concepts when running this application, serving existing content, and editing/creating new content.  However, where this content lives is somewhat complicated.

## Serving

To support both a preview and a produciton instance, there are three main instances of this repository on the server:

1. The first is the main one that is checked out and running the nginx, uWSGI, and scorsese.  These bits rarely change, if ever.  If they do change, they will be done separately from the content updates.
2. The other two are for static files served by nginx to show the development and production content.  These are managed by scorsese and are generated on the fly based on commands from the UI.  Nginx is configured to serve these contents from fixed paths.  The contents themselves are edited and updated by the flask server named scorsese.

## Editing

When editing content using the scorsese UI, there are two possible destinations:

* **Development** is just a staging area that isn't commited and is not visible to the public.  Drafts are rendered here so that the person writing content and editing can preview what the result will look like before publishing.
* **Production** is what external people can see.  Drafts are not rendered.  Only content that has been pushed to master is rendered.

Both of these destinations are managed by scorsese and served by nginx.

When an edit is made, it goes through the following flow from conception to production:

1. The user will either create a new page, or edit an existing one.
2. The user will use the provided editor to create content.
3. The user can either back out (unsaved) or "push to staging".
4. The server will apply the change to the development directory, rebuild, and redirect the user back to the index.
5. The user can view the available changes.
6. The user can then select "push to production" from the index.
7. The server will stage all content changes in development, commit, push, and then pull onto production.

nginx will automatically serve the contents of those folders so no other changes are necessary.

# Configuration

This section talks about "configuration" that is tracked in version control in this repository, that isn't code.  This is mostly to track why nginx and uWSGI are set up the way they are and how to interpret their properties.

Keep in mind that the "development" and "production" aspects of content distribution do not apply here.  Configuration for nginx and uWSGI are all under the master directory and there is only ever one of it on the server.  Deploys to the configuration for these are special.

# Externals

Beyond code, there's some things that must be documented, like server configuration and external dependencies not covered by code or configuration.  While they are external to this repository, they are critical to running this service.

Most of this is related to the FreeBSD instance we get from NearlyFreeSpeech, but it's worth documenting since these are specific to maintaining the one instance that matters.

## DNS

DNS Registrations:
* aggressivelyparaphrasing.me is managed by namecheap.com
* [href.cat](href.cat) is managed by gandi.net

DNS Records:
* MX for [href.cat](href.cat) for email
* ALIAS aggressivelyparaphrasing.me to the domain provided by nearlyfreespeech.net
* ALIAS www.aggressivelyparaphrasing.me to the domain provided by aggressivelyparaphrasing.me
* ALIAS dev.aggressivelyparaphrasing.me to the domain provided by nearlyfreespeech.net
* ALIAS admin.aggressivelyparaphrasing.me to the domain provided by nearlyfreespeech.net
* ALIAS [href.cat](href.cat) to the domain provided by nearlyfreespeech.net

nginx runs on the nearlyfreespeach.net host and uses the HOST header to point specific servers to directores or processes


## Git

NearlyFreeSpeech came with git installed.

I just needed to generate keys based on [GitHub docs](https://help.github.com/en/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent "Generating a new SSH key and adding it to the ssh-agent"):

```
ssh-keygen -t rsa -b 4096 -C "aggressivelyparaphrasingme@nearlyfreespeech.net"
```

Then add them to [my GitHub account's authroized keys](https://github.com/settings/keys).

This allowed me to run the clone:
```
git clone git@github.com:nguyenmp/aggressivelyparaphrasing.me.git
```

Then initialize the prod and dev sites:

```
git clone git@github.com:nguyenmp/aggressivelyparaphrasing.me.git ~/prod/
cp -r ~/prod/ ~/dev/
hugo --source ~/prod/hugo
hugo -D --source ~/dev/hugo
```

## Nginx
I configured NearlyFreeSpeech to have a custom HTTP server.

Then I built nginx from scratch cause I didn't have privileges to install using the package manager and I couldn't figure out ports.  I need the --prefix argument to configure to prevent it from running against hard-coded paths in /usr/local/nginx which is owned by root on NearlyFreeSpeech.  Instead, I set it to /home/private/nginx which is in my personal user's space and created by me.  This idea wasn't novel to me, it was [described by Perlkonig
on the member's support forum](https://members.nearlyfreespeech.net/forums/viewtopic.php?t=8813) in passing and I found it very insightful and inspiring.

Download and build from source.  This is mostly taken from [the official guide](http://nginx.org/en/docs/configure.html):

```
curl http://nginx.org/download/nginx-1.17.2.tar.gz -o nginx-1.17.2.tar.gz
tar -zxvf nginx-1.17.2.tar.gz
mkdir nginx
cd nginx-1.17.2
./configure --prefix=/home/private/nginx
make
```

Create the logging folder that nginx is configured to use.  This must be done or else the latter nginx invocation will fail to launch:

```
mkdir /home/private/nginx/logs/
```

Install the default configuration, then our own on top:
```
mkdir ~/nginx/conf/
cp -r ~/nginx-1.17.2/conf ~/nginx/conf/
rm ~/nginx/conf/nginx.conf
ln -s ~/aggressivelyparaphrasing.me/nginx/nginx.conf ~/nginx/conf/nginx.conf
```

Then launch the nginx binary that we just built:
```
~/nginx-1.17.2/objs/nginx
```

## Proxy

In the NearlyFreeSpeech admin console, I added a "proxy" which I think just describes how to forward requests against certain roots and ports to which ports and additional roots.  In my case, since I cannot run nginx as root without root access, I cannot listen to port 80.  Thus, I listen to port 8080 instead.

In the admin panel, I add the following:
| Field | Value |
|--|----|
| Protocol | HTTP |
| Base URL | / |
| Document Root | / |
| Target Port | 8080 |

Most of the values like Base URL and Document Root are things I can configure in nginx, and I prefer to keep them in source control anyways.  Really, I just need to set the target port to get the job done.

## uWSGI

It was already installed so I did nothing.

```
$ pip3 install uwsgi
Requirement already satisfied: uwsgi in /usr/local/lib/python3.7/site-packages (2.0.18)
```

I did have to install the dependency packages though:

```
pip3 install -e ~/aggressivelyparaphrasing.me/scorsese/ --user
```

## Daemon

I also configured the a daemon that runs nginx:

| Field | Value |
|--|----|
| Tag | nginxtag |
| Command Line | /home/private/nginx-1.17.2/objs/nginx |
| Working Directory | /home/public (this doesn't really matter) |
| Run Daemon As | me (web doesn't work because permissions) |

And one that runs the python admin code:

| Field | Value |
|--|----|
| Tag | scorsesetag |
| Command Line | /home/private/aggressivelyparaphrasing.me/uwsgi/run.sh |
| Working Directory | /home/public (this doesn't really matter) |
| Run Daemon As | me (web doesn't work because permissions) |


## SSL/TSL

> If you don't already have a certificate provider, the most popular option is Let's Encrypt, a free service. The easiest way to use Let's Encrypt certificates is to type the following command in the shell:

> `YourPrompt> tls-setup.sh`

So that's what I did...  I don't think it worked.

I noticed that the "well known" challenge failed.  It was also noted in the FAQ, they mention it might not work with special web daemons (like nginx).

> This script handles the simplest, most common cases. If your site uses custom web daemons or custom access controls, the automatic scripts may not work for you. For such cases, we provide the dehydrated ACME client; it provides hooks to install and clean up challenges that you can use to interface with whatever you're doing.
> 
> [How do I set up HTTPS (TLS) for my web site?
](https://members.nearlyfreespeech.net/faq?q=SSLCertificates#SSLCertificates)

I dug around and found the ["Well Known" docs in dehydrated](https://github.com/lukas2511/dehydrated/blob/master/docs/wellknown.md).  Apparently, well known is a form of challenge and I was lucky enough to notice this line:

```
# INFO: Using main config file /usr/local/etc/dehydrated/config
```

And that pointed me to:

```bash
$ cat /usr/local/etc/dehydrated/config
AUTO_CLEANUP='yes'
BASEDIR='/home/private/.dehydrated/'
WELLKNOWN='/home/public/.well-known/acme-challenge/'
HOOK='/usr/local/lets-nfsn.sh/nfsn-hook.sh'
```

So in the end, I figured I just needed to add the following line to all my servers in my nginx.conf:

```
server {
  [...]
  location ^~ /.well-known/acme-challenge {
    alias /home/public/.well-known/acme-challenge/;
  }
  [...]
}
```

It sounds like NearlyFreeSpeech will automatically run this command for me so as long as it works I'll always be rotating my certificates before expiry.  That also means I need to keep the well known paths for my domains to automatically prove they are in my possession.

In the end, the command worked after adding the above well-known routes:

```
$ tls-setup.sh
```

Finally, in the NearlyFreeSpeech admin panel for the website, I enabled "Canonical HTTPS".  I think what's happening is NearlyFreeSpeech is running an HTTP server in front of all their customers and downgrading the connection security on their end before it reaches us.  This allows them to do cool things like HTTP rewrites for us, but it also means connections to me aren't on traditional ports like 443 or 80.  I can't use the port number to determine if the connection is secure because it's 8080.

## TODO

Although not set up yet, I intend to:
1. set up email from mxroute.com
2. Set up mail forwarding from DNS

# Deploys

SSH information is available from NearlyFreeSpeech.NET.

For only the HTML from hugo, use the admin page:
* You can reset prod to latest master
* You can reset dev to any branch, we will reclone to get latest remote
* Any edits through the web-UI will automatically be built and deployed to dev

For changes to scorsese (aka python), you will need to SSH into the machine, do a git pull on ~/aggressivelyparaphrasing.me/, then in the NearlyFreeSpeech.net web-UI, send a "KILL" signal to "scorsesetag".  On that same page, you should eventually see under "Recent Event Logs": "Daemon scorsesetag stopped" and "Fast start requested for daemon scorsesetag".

For config changes to nginx, do a git pull, then `nginx -s reload` or something like that.  Use the custom built nginx, and double check reload is the right argument using `nginx -h`.

For config changes to uWSGI, edit the run.sh file and then send the "KILL" signal to "scorsesetag".

SSH information is available from NearlyFreeSpeech.NET and the password is somewhere good.

# Local Setup

How to run and test at desk:

## Nginx webserver

1. Install nginx: `brew install nginx`
2. Install the nginx config file: `ln -s nginx/nginx.conf /usr/local/etc/nginx/nginx.conf` 
3. Make nginx pick up the changes: `nginx` or `nginx -s reload`, depending on if it's already running
4. Add the following to your `/etc/hosts` for local development to redirect DNS pointers to your local machine.  This allows you to test nginx stuff still:
```
127.0.0.1	aggressivelyparaphrasing.me
127.0.0.1	dev.aggressivelyparaphrasing.me
127.0.0.1	admin.aggressivelyparaphrasing.me
```
5. Launch the admin python server: `cd aggressivelyparaphrasing/scorsese && uwsgi --socket 127.0.0.1:3031 --wsgi scorsese --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191`
6. Create a folder for the development static site: `git clone git@github.com:nguyenmp/aggressivelyparaphrasing.me.git /usr/local/etc/ap_dev`
7. Build the dev static site with drafts: `hugo -D --source /usr/local/etc/ap_dev/hugo`
8. Create a folder for the production static site: `git clone git@github.com:nguyenmp/aggressivelyparaphrasing.me.git /usr/local/etc/ap_prod`
9. Build the prod static site without drafts: `hugo --source /usr/local/etc/ap_prod/hugo`

## Only scorsese

1. Edit scorsese/__init__.py to use ./container instead of /home/private
2. Run `FLASK_APP=scorsese FLASK_DEBUG=True python3 -m flask run`

## Only hugo

1. Run `hugo -D --source hugo/` to build with drafts
