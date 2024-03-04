#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'nomw',
        version = '0.0.1.dev20240303214017',
        description = 'Node-On-My-Watch (NOMW) is a utility for keeping K8S EC2 nodes fresh by killing them off while ensuring the running workload remains stable',
        long_description = '# Node-On-My-Watch (NOMW)\n\n[![Gitter](https://img.shields.io/gitter/room/karellen/lobby?logo=gitter)](https://gitter.im/karellen/Lobby)\n[![Build Status](https://img.shields.io/github/actions/workflow/status/karellen/node-on-my-watch/node-on-my-watch.yml?branch=master)](https://github.com/karellen/node-on-my-watch/actions/workflows/node-on-my-watch.yml)\n[![Coverage Status](https://img.shields.io/coveralls/github/karellen/node-on-my-watch/master?logo=coveralls)](https://coveralls.io/r/karellen/node-on-my-watch?branch=master)\n\n[![Node-On-My-Watch Version](https://img.shields.io/pypi/v/nomw?logo=pypi)](https://pypi.org/project/nomw/)\n[![Node-On-My-Watch Python Versions](https://img.shields.io/pypi/pyversions/nomw?logo=pypi)](https://pypi.org/project/nomw/)\n[![Node-On-My-Watch Downloads Per Day](https://img.shields.io/pypi/dd/nomw?logo=pypi)](https://pypi.org/project/nomw/)\n[![Node-On-My-Watch Downloads Per Week](https://img.shields.io/pypi/dw/nomw?logo=pypi)](https://pypi.org/project/nomw/)\n[![Node-On-My-Watch Downloads Per Month](https://img.shields.io/pypi/dm/nomw?logo=pypi)](https://pypi.org/project/nomw/)\n\n## Notices\n\n### Beta Software\n\nWhile fully functional in the current state and used in production, this software is in **BETA**.\nDocumentation at this stage is basically non-existent.\n\n### License\n\nThe product is licensed under the Apache License, Version 2.0. Please see LICENSE for further details.\n\n### Warranties and Liability\n\nNode-On-My-Watch is provided on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either\nexpress or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT,\nMERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE. You are solely responsible for determining the appropriateness of\nusing or redistributing Node-On-My-Watch and assume any risks associated with doing so.\n\n### Trademarks\n\n"Node-On-My-Watch" and "NOMW" are trademarks or registered trademarks of Karellen, Inc. \nAll other trademarks are property of their respective owners.\n\n## Problem Statement\n\n## Solution\n\n## Using Node-On-My-Watch with Docker\n\nA simple example is as follows:\n```\n$ docker run -t ghcr.io/karellen/node-on-my-watch:latest\n```\n\n## Using Node-On-My-Watch on MacOS\n\n```\n$ brew install python3.11\n$ pip3.11 install nomw\n$ nomw --version\n```\n',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX',
            'Operating System :: POSIX :: Linux',
            'Environment :: Console',
            'Topic :: Utilities',
            'Topic :: System :: Monitoring',
            'Topic :: System :: Distributed Computing',
            'Topic :: System :: Clustering',
            'Topic :: System :: Networking',
            'Intended Audience :: System Administrators',
            'Intended Audience :: Developers',
            'Development Status :: 4 - Beta'
        ],
        keywords = 'kubernetes k8s kube AWS node',

        author = 'Karellen, Inc.',
        author_email = 'supervisor@karellen.co',
        maintainer = 'Karellen, Inc., Arcadiy Ivanov',
        maintainer_email = 'supervisor@karellen.co,arcadiy@karellen.co',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/karellen/node-on-my-watch',
        project_urls = {
            'Bug Tracker': 'https://github.com/karellen/node-on-my-watch/issues',
            'Documentation': 'https://github.com/karellen/node-on-my-watch/',
            'Source Code': 'https://github.com/karellen/node-on-my-watch/'
        },

        scripts = [],
        packages = ['karellen.nomw'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {
            'console_scripts': ['nomw = karellen.nomw:main']
        },
        data_files = [],
        package_data = {
            'kubernator': ['LICENSE']
        },
        install_requires = [
            'boto3~=1.34',
            'coloredlogs~=15.0',
            'gevent>=21.1.2',
            'json-log-formatter~=0.3',
            'kubernetes~=29.0',
            'platformdirs~=4.2',
            'requests~=2.25'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '>=3.9',
        obsoletes = [],
    )
