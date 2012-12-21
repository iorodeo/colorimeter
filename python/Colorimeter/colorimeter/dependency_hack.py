"""
Hack for dealing with missing item from list of hiddenimports
in scipy hook.  This should be removed when it is fixed in later
version of pyinstaller.
"""

def pyinstaller_dependency_hack():
    from scipy.sparse.csgraph import _validation
