'''
Wrapper around hugo commands and interacting with hugo files and abstractions
'''

import os
import re
import subprocess

import yaml
import frontmatter as parser

def build(hugo_path, with_drafts=False):
    '''
    Runs the "hugo build" command on the given path
    '''
    subprocess.check_call([
        'hugo',
        '--source', hugo_path,
        '--buildDrafts='+str(with_drafts),
        '--enableGitInfo',
    ])


def new(hugo_path, name):
    '''
    Creates a new item in the given archetype.  For example,
    (name=posts/first-post) will run "hugo new posts/first-post.md".
    '''
    # Clean input
    assert not name.endswith('.md')
    assert re.match('^[_a-zA-Z-][_/a-zA-Z-]+$', name)  # Must not start with slash

    name = name + '.md'
    subprocess.check_call([
        'hugo',
        '--source', hugo_path,
        'new', name,
    ])


def get_content_file(path):
    '''
    Given a path, returns the full content and the parsed front matter as a tuple.
    '''
    with open(path, 'r') as handle:
        content = handle.read()

    frontmatter = None
    try:
        frontmatter = parser.loads(content)
    except yaml.parser.ParserError as e:
        print(e)
    return (content, frontmatter)


def get_content_files(hugo_path):
    '''
    Scans the relative file system for the content files to administer

    This is the hugo/content/ files that we can edit and manipulate
    '''
    pattern = '^.*\\.md$'
    contents_dir = os.path.join(hugo_path, 'content', '')
    for dirpath, _dirnames, filenames in os.walk(contents_dir):
        for filename in filenames:
            if re.match(pattern, filename):
                full_path = os.path.join(dirpath, filename)
                _content, frontmatter = get_content_file(full_path)
                short_path = full_path[len(contents_dir):]  # Make path relative to hugo/content/
                url_path = get_url_path(short_path)
                yield (url_path, short_path, frontmatter)


def get_url_path(short_path):
    '''
    Given the path under the "content" folder of hugo, return the expected URL path.

    For example:
    _index.md => /
    posts/oreo-paper.md => posts/oreo-paper/
    sample.md => sample/
    '''
    return re.sub('(_index\.md|\.md)', '/', short_path)
