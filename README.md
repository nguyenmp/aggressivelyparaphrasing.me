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

Although not set up yet, I intend to:
1. get the domain from NameCheap
2. set up the SSL certificate with LetsEncrypt
3. set up hosting from https://www.nearlyfreespeech.net
4. set up email from mxroute.com
5. Set up mail forwarding from DNS