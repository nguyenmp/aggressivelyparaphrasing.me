import os
import shutil
import subprocess

from flask import Flask, request, render_template

from . import git, hugo

app = Flask(__name__)

CONTAINER = './container'
PREVIEW_PATH = os.path.join(CONTAINER, 'preview')
PROD_PATH = os.path.join(CONTAINER, 'production')
REPOSITORY = None


@app.route('/admin')
def index():
    '''
    Lists all the available posts, their content
    '''
    return render_template('list.html', content_files=hugo.get_content_files())


@app.route('/admin/edit', methods=["GET"])
def get_edit():
    path = request.args['path']
    content, _frontmatter = hugo.get_content_file(path)
    return render_template('item.html', content=content)


@app.route('/admin/edit', methods=["POST"])
def post_edit():
    path = None
    content = None
    if True:
        return preview(path, content)
    else:
        save(path, content)
        return self
    raise Exception('Not Implemented yet!')


def preview(path, content):
    '''
    Apply the given content to the preview subdomain.  The build the preview
    data with drafts.  Then redirect the user to the given page on the
    preview subdomain.  Basically integration testing!
    '''
    reinitialize_preview_files()
    apply_change_to_preview(path, content)
    hugo.build(PREVIEW_PATH, with_drafts=True)


def apply_change_to_preview(path, content):
    '''
    Writes the given content to the given path
    '''
    with open(os.path.join(PREVIEW_PATH, path), 'w') as handle:
        handle.write(content)


def reinitialize_preview_files():
    '''
    Nukes any existing content from the preview path and starts off clean from
    master.  This means that content should always be up to date.
    '''
    shutil.rmtree(PREVIEW_PATH)
    directory, name = os.path.split(PREVIEW_PATH)
    git.clone(directory, REPOSITORY, name)


def save(path, content):
    '''
    Make the change, save it to git, and update the prod server with the change
    '''
    # Apply changes to the preview path
    preview(path, content)

    # Save the preview path to master
    git.commit(PREVIEW_PATH, message)
    git.push(PREVIEW_PATH)

    # Tell prod path to pull from master
    update_prod()


def update_prod():
    '''
    Updates the static files for the prod deploy of the hugo static site
    '''
    git.ensure_up_to_date_and_unchanged(PROD_PATH)
    hugo.build(PROD_PATH, with_drafts=False)
    git.ensure_up_to_date_and_unchanged(PROD_PATH)
