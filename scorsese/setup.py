'''
Borrowed from https://flask.palletsprojects.com/en/1.1.x/patterns/packages/


'''

from setuptools import setup

setup(
    package_name="scorsese",
    install_requires=[
        'flask',
        'python-frontmatter',
    ],
)
