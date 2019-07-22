'''
Wrapper API around git commands
'''

import subprocess

def commit(path, message):
    '''
    Runs "git commit" from the given path with the
    given message, adding any paths by default
    '''
    subprocess.check_call([
        'git',
        '-C', path,
        'commit',
        '-am',
        message,
    ])


def push(path):
    '''
    Runs "git push" on the given path
    '''
    # git push
    subprocess.check_call([
        'git',
        '-C', path,
        'push',
    ])


def ensure_up_to_date_and_unchanged(path):
    '''
    Make sure we're up to date and that we don't have any unsaved changes applied
    '''
    # Make sure there's no unsaved changes
    subprocess.check_call([
        'git',
        '-C', path,  # Run the command from the path provided
        'diff-index', 'origin/master',  # Run the diff against remote's master
        '--quiet',   # The output is the return code, instead of standard output
    ])

    # Then update to the latest remote changes
    subprocess.check_call([
        'git',
        '-C', path,
        'pull'
    ])


def clone(directory, repository, name):
    '''
    Clone the given repository into the given directoy
    using the given name for the target folder to clone as.
    '''
    subprocess.check_call([
        'git',
        '-C', directory,
        'clone', repository, name,
    ])
