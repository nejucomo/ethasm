#!/usr/bin/env python

import os, sys, subprocess
from setuptools import setup, find_packages, Command


PACKAGE = 'ethasm'
INSTALL_REQUIRES = [
    'pyethereum >= 0.2.4',
    'twisted >= 14.0',
    'mock >= 1.0.1',
    ]


def main(args = sys.argv[1:]):
    setup(
        name=PACKAGE,
        description='Ethereum assembler / disassembler.',
        version='0.1.dev0',
        author='Nathan Wilcox',
        author_email='nejucomo@gmail.com',
        license='GPLv3',
        url='https://github.com/nejucomo/{0}'.format(PACKAGE),

        packages=find_packages(),

        entry_points={
            'console_scripts': [
                '{0} = {0}.commandline:main'.format(PACKAGE),
                ],
            },

        install_requires=INSTALL_REQUIRES,

        cmdclass={
            'test': TestWithCoverageAndTrialInAVirtualEnvCommand,
            },
        )


class TestWithCoverageAndTrialInAVirtualEnvCommand (Command):
    """Run unit tests with coverage analysis and reporting in a virtualenv.

    Note: A design goal of this is that all generated files (except for
    .pyc files) will appear under ./build so that .gitignore can contain
    only ./build and *.pyc, and a clean operation is merely 'rm -r ./build'.
    """

    TestToolRequirements = [
        'coverage == 3.7.1',
        ]

    user_options = [
        ]

    def __init__(self, dist):
        Command.__init__(self, dist)
        join = os.path.join

        self.basedir = os.path.dirname(os.path.abspath(__file__))
        self.pypkg = join(self.basedir, PACKAGE)
        self.testdir = join(self.basedir, 'build', 'test')
        self.venvdir = join(self.testdir, 'venv')

        self.bindir = os.path.join(self.venvdir, 'bin')
        self.trial = os.path.join(self.bindir, 'trial')
        self.pip = os.path.join(self.bindir, 'pip')
        self.coverage = os.path.join(self.bindir, 'coverage')

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self._initialize_virtualenv()
        self._install_testing_tools()
        self._update_python_path()

        # Coverage and trial dump things into cwd, so cd:
        os.chdir(self.testdir)

        try:
            run(self.coverage, 'run', '--branch', '--source', self.pypkg, self.trial, PACKAGE)
        finally:
            run(self.coverage, 'html')

    def _initialize_virtualenv(self):
        run('virtualenv', '--no-site-packages', self.venvdir)

    def _install_testing_tools(self):
        reqspath = os.path.join(self.testdir, 'test-tool-requirements.txt')

        with file(reqspath, 'w') as f:
            for req in INSTALL_REQUIRES + self.TestToolRequirements:
                f.write(req + '\n')

        run(self.pip, 'install', '--use-mirrors', '--requirement', reqspath)

    def _update_python_path(self):
        if 'PYTHONPATH' in os.environ:
            os.environ['PYTHONPATH'] = '{0}:{1}'.format(self.basedir, os.environ['PYTHONPATH'])
        else:
            os.environ['PYTHONPATH'] = self.basedir


def run(*args):
    print 'Running: {0!r}'.format(args)
    try:
        subprocess.check_call(args, shell=False)
    except subprocess.CalledProcessError, e:
        print 'Process exited with {0!r} exit status.'.format(e.returncode)
        raise



if __name__ == '__main__':
    main()
