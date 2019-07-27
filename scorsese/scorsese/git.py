'''
Wrapper API around git commands
'''

import collections
import re
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


def checkout(path, branch):
    '''
    Runs "git -C {{path}} checkout {{branch}}" on the given path
    '''
    subprocess.check_call([
        'git',
        '-C', path,
        'checkout',
        branch,
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

def status(path):
    'Adds all unstaged files and then returns the resulting "status" as a pair of modifications and file path'

    # Add all contents to staging area
    subprocess.check_call([
        'git',
        '-C', path,
        'add', '.',
    ])

    # Run parsable git-status
    output = subprocess.check_output([
        'git',
        '-C', path,
        'status', '--porcelain'
    ]).decode('utf8')

    # Parse output
    return [parse_porcelain_line(line) for line in output.splitlines()]


def diff(container, path):
    '''
    Returns the output of running git diff on the given file

    Takes the folder that has the .git in it, and the path to show the cached diff with
    '''
    return subprocess.check_output([
        'git', 'diff',
        '--cached',
        path,
    ], cwd=container).decode('utf8')


def parse_porcelain_line(line):
    '''
    Returns a Change tuple, parsed from a single line of porcelain output
    '''
    match = re.match('^(M|A|D|R|C)  (.*)$', line)
    short_name = match.group(1)
    target = match.group(2)
    description = SHORT_NAME_TO_DESCRIPTION[short_name]

    # Parse out the source and destination for renames and copies
    source = None
    destination = None
    match = re.match('^(.*) -> (.*)$', target)
    if match:
        source = match.group(1)
        destination = match.group(2)

    # Group them all into a tuple and return
    return Change(
        short_name=short_name,
        description=description,
        target=target,
        source=source,
        destination=destination,
    )


Change = collections.namedtuple('Person', [
    'short_name',  # The character describing the type of change
    'description',  # The english word that describes the type change
    'target',  # The target for this change; either the filename or "source -> destination"
    'source',  # Only used for rename and copy; left side of "->"
    'destination',  # Only used for rename and copy; right side of "->"
])


SHORT_NAME_TO_DESCRIPTION = {
    'M': 'Modified',
    'A': 'Added',
    'D': 'Deleted',
    'R': 'Renamed',
    'C': 'Copied',
}