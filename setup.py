#!/usr/bin/env python
# encoding: utf-8

__version__ = "$Revision$"

import os
import sys
from fnmatch import fnmatchcase
from distutils.util import convert_path
from setuptools import setup, find_packages

if sys.version_info <= (2, 3):
    raise SystemExit("Python 2.3 or later is required.")

execfile(os.path.join("turbomail", "release.py"))

def find_package_data( package='', where='.', only_in_packages=True):
    """Finds static resources in package. Adapted from turbogears.finddata."""  
    out = {}
    exclude = ('*.py', '*.pyc', '*.pyo', '*~', '.*', '*.bak', '*.swp*')
    exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')
    stack = [(convert_path(where), '', package, only_in_packages)]
    while stack:
        where, prefix, package, only_in_packages = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
#                        print >> sys.stderr, (
#                            "Directory %s ignored by pattern %s"
#                            % (fn, pattern))
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                    stack.append((fn, '', new_package, False))
                else:
                    stack.append((fn, prefix + name + '/', package, only_in_packages))
            elif package or not only_in_packages:
                # is a file
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
#                        print >> sys.stderr, (
#                            "File %s ignored by pattern %s"
#                            % (fn, pattern))
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out

install_requires = []

setup(
        name="TurboMail",
        version=version,
        
        description=description,
        long_description=long_description,
        author=author,
        author_email=email,
        url=url,
        download_url=download_url,
        license=license,
        
        install_requires = install_requires,
        extras_require = {
            'turbogears': ["TurboMail-Gears >= 0.1"],
        },
        
        zip_safe=True,
        packages=find_packages(),
        package_data = find_package_data(where='turbomail', package='turbomail'),
        classifiers = [
            'Development Status :: 5 - Production/Stable',
            'Framework :: TurboGears',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Communications :: Email',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
        test_suite = 'nose.collector',
        tests_require = 'pymta >= 0.3',
        entry_points = {
            'turbomail.managers': [
                "demand = turbomail.managers.demand",
                "immediate = turbomail.managers.immediate"
            ],
            'turbomail.transports': [
                "smtp = turbomail.transports.smtp",
                "debug = turbomail.transports.debug"
            ],
            'turbomail.extensions': [
                "utf8qp = turbomail.extensions.utf8qp",
            ],
            'turbogears.extensions': ["turbomail = turbomail.adapters.tg1"]
        }
    )
    
