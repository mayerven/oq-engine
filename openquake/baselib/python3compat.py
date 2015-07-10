#  -*- coding: utf-8 -*-
#  vim: tabstop=4 shiftwidth=4 softtabstop=4

#  Copyright (c) 2015, GEM Foundation

#  OpenQuake is free software: you can redistribute it and/or modify it
#  under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  OpenQuake is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU Affero General Public License
#  along with OpenQuake.  If not, see <http://www.gnu.org/licenses/>.

"""
Compatibility layer for Python 2 and 3. Mostly copied from six and future,
but reduced to the subset of utilities needed by GEM. This is done to
avoid an external dependency.
"""
from __future__ import print_function
import os
import sys
import importlib
import subprocess

PY3 = sys.version_info[0] == 3
PY2 = sys.version_info[0] == 2

if PY3:
    range = range

    def raise_(tp, value=None, tb=None):
        """
        A function that matches the Python 2.x ``raise`` statement. This
        allows re-raising exceptions with the cls value and traceback on
        Python 2 and 3.
        """
        if value is not None and isinstance(tp, Exception):
            raise TypeError("instance exception may not have a separate value")
        if value is not None:
            exc = tp(value)
        else:
            exc = tp
        if exc.__traceback__ is not tb:
            raise exc.with_traceback(tb)
        raise exc

else:  # Python 2
    range = xrange

    exec('''
def raise_(tp, value=None, tb=None):
    raise tp, value, tb
''')


# copied from http://lucumr.pocoo.org/2013/5/21/porting-to-python-3-redux/
def with_metaclass(meta, *bases):
    """
    Returns an instance of meta inheriting from the given bases.
    To be used to replace the __metaclass__ syntax.
    """
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__

        def __new__(mcl, name, this_bases, d):
            if this_bases is None:
                return type.__new__(mcl, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})


def check_syntax(pkg):
    """
    Recursively check all modules in the given package for compatibility with
    Python 3 syntax. No imports are performed.

    :param pkg: a Python package
    """
    ok, err = 0, 0
    for cwd, dirs, files in os.walk(pkg.__path__[0]):
        for f in files:
            if f.endswith('.py'):
                fname = os.path.join(cwd, f)
                errno = subprocess.call(['python3', '-m', 'py_compile', fname])
                if errno:
                    err += 1
                else:
                    ok += 1
    print('Checked %d ok, %d wrong modules' % (ok, err))


if __name__ == '__main__':
    check_syntax(importlib.import_module(sys.argv[1]))
