'''
Wrapper around hugo commands and interacting with hugo files and abstractions
'''

import os
import re
import subprocess

import frontmatter

def build(path, with_drafts=False):
    '''
    Runs the "hugo build" command on the given path
    '''
    subprocess.check_call([
        'hugo', 'build',
        '--source', path,
        '--buildDrafts', 'true' if with_drafts else 'false',
    ])


def get_content_file(path):
    '''
    Given a path, returns the full content and the parsed front matter as a tuple.
    '''
    with open(path, 'r') as handle:
        content = handle.read()

    frontmatter = frontmatter.loads(content)
    return (content, frontmatter)


def get_content_files():
    '''
    Scans the relative file system for the content files to administer

    This is the hugo/content/ files that we can edit and manipulate
    '''
    pattern = r'^.*\.md$'
    for dirpath, _dirnames, filenames in os.walk('../hugo/content/'):
        for filename in filenames:
            if re.match(pattern, filename):
                full_path = os.path.join(dirpath, filename)
                _content, frontmatter = get_content_file(full_path)
                yield (full_path, frontmatter)
