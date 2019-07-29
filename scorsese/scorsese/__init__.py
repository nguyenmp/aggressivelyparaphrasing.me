import base64
import functools
import hashlib
import io
import os
import re
import shlex
import shutil
import subprocess

from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    Response,
    abort,
)

from . import git, hugo

app = Flask(__name__)
app.config['SECRET_KEY'] = base64.b64decode(os.environ['SECRET_KEY'])

CONTAINER = '/home/private'
PREVIEW_DIR_NAME = 'dev'
PROD_DIR_NAME = 'prod'
PREVIEW_PATH = os.path.join(CONTAINER, PREVIEW_DIR_NAME)
PREVIEW_HUGO_PATH = os.path.join(PREVIEW_PATH, 'hugo')
PROD_PATH = os.path.join(CONTAINER, PROD_DIR_NAME)
PROD_HUGO_PATH = os.path.join(PROD_PATH, 'hugo')
REPOSITORY = 'git@github.com:nguyenmp/aggressivelyparaphrasing.me.git'


def try_init():
    '''
    Creates the container and the sub folders.

    Ignores any individual if htey already exist.  If container exist, just use
    it.  If either dev or prod already exists, use those.  No deletion or
    overriding.  Only clone or mkdir if it doesn't exist.
    '''
    if not os.path.exists(CONTAINER):
        print('Making container')
        os.mkdir(CONTAINER)
    else:
        print('Container already exists')

    if not os.path.exists(PREVIEW_PATH):
        print('Making dev')
        git.clone(CONTAINER, REPOSITORY, PREVIEW_DIR_NAME)
    else:
        print('Dev already exists')

    if not os.path.exists(PROD_PATH):
        print('Making prod')
        git.clone(CONTAINER, REPOSITORY, PROD_DIR_NAME)
    else:
        print('Prod already exists')


def check_csrf(callee):
    '''
    A decorator for wrapping routes that one wants to have check csrf on

    These routes should accept POSTs and should have a csrf field submitted

    The value of these fields should be set to the return of get_csrf.
    '''
    @functools.wraps(callee)
    def caller(*args, **kwargs):
        csrf = request.form['csrf']
        if not csrf or get_csrf() != csrf:
            abort(401)
        return callee(*args, **kwargs)

    return caller


@app.route('/')
def index():
    '''
    Lists all the available posts, their content
    '''
    return render_template(
        'list.html',
        content_files=hugo.get_content_files(PREVIEW_HUGO_PATH),
        status=git.status(PREVIEW_PATH),
        csrf=get_csrf(),
    )


@app.route('/post', methods=["GET"])
def get():
    '''
    Returns the HTML/UI for editing a post
    '''
    relative_path = request.args['path']
    full_path = os.path.join(PREVIEW_HUGO_PATH, 'content', relative_path)
    content, _frontmatter = hugo.get_content_file(full_path)
    return render_template(
        'item.html',
        content=content,
        shortpath=relative_path,
        csrf=get_csrf(),
    )


@app.route('/post', methods=["POST"])
@check_csrf
def edit():
    old_path = request.form['old_path']
    new_path = request.form['new_path']
    content = request.form['content']

    # Note, we set newline here because HTML5 spec specifies to return form
    # content with \r\n canonicalized newline ending but we store the files in
    # git with linux newline \n.  To maintain consistent diffs on contents, we
    # always write with \n.
    content = re.sub('\r\n', '\n', content)

    os.remove(os.path.join(PREVIEW_HUGO_PATH, 'content', old_path))
    with io.open(os.path.join(PREVIEW_HUGO_PATH, 'content', new_path), 'w', newline='\n') as handle:
        handle.write(content)

    # Remember to rebuild, or else it won't show up in the preview
    hugo.build(PREVIEW_HUGO_PATH, with_drafts=True)

    return redirect(url_for('index'))


@app.route('/diff', methods=["GET"])
def diff():
    relative_path = request.args['path']
    return render_template('diff.html', content=git.diff(PREVIEW_PATH, relative_path))


@app.route('/new', methods=["POST"])
@check_csrf
def create():
    name = request.form['file_name']
    hugo.new(PREVIEW_HUGO_PATH, name)
    hugo.build(PREVIEW_HUGO_PATH, with_drafts=True)
    return redirect(url_for('index'))


@app.route('/reset', methods=["POST"])
@check_csrf
def reset():
    name = request.form['environment']
    branch = request.form['branch']
    recreate(name, branch)
    return redirect(url_for('index'))


@app.route('/save', methods=["POST"])
@check_csrf
def save():
    # Make sure we don't save unbuildable stuff
    hugo.build(PREVIEW_HUGO_PATH, with_drafts=False)
    hugo.build(PREVIEW_HUGO_PATH, with_drafts=True)

    # Push to remote git server
    message = "[Automated] {}".format(
        ', '.join(change.description + ' ' + change.target for change in git.status(PREVIEW_PATH))
    )
    git.commit(PREVIEW_PATH, message)
    git.push(PREVIEW_PATH)

    # Repull our web server's data from remote git server
    recreate("dev")
    recreate("prod")

    return redirect(url_for('index'))


def recreate(environment, branch=None):
    '''
    Nukes any existing content from the environment's path and starts off
    clean from master.  This means that content should always be up to date.

    environment is either "dev" or "prod"
    '''
    print("Recreating")
    if environment == 'dev':
        path = PREVIEW_PATH
        hugo_path = PREVIEW_HUGO_PATH
        with_drafts = True
    elif environment == 'prod':
        path = PROD_PATH
        hugo_path = PROD_HUGO_PATH
        with_drafts = False
    else:
        raise Exception('Unknown environment: {}'.format(environment))

    shutil.rmtree(path)
    directory, name = os.path.split(path)
    git.clone(directory, REPOSITORY, name)
    if branch:
        git.checkout(path, branch)
    hugo.build(hugo_path, with_drafts=with_drafts)
    print("Recreated")


def get_csrf():
    '''
    Returns the csrf token for the given authenticated user
    '''
    if not app.secret_key or not hasattr(request.authorization, 'username'):
        return None

    h = hashlib.sha256(app.secret_key)
    h.update(request.authorization.username.encode('utf8'))
    return h.hexdigest()


@app.errorhandler(401)
def custom_401(error):
    return Response('Unauthorized', 401, {'WWW-Authenticate':'Basic realm="Not allowed"'})


try_init()
