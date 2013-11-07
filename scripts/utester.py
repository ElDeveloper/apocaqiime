#!/usr/bin/env python
__author__ = "Yoshiki Vazquez-Baeza"
__license__ = "GPL"
__version__ = "1.0.0-dev"
__maintainer__ = "Yoshiki Vazquez-Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Use at your own risk"


from sys import argv
from os.path import split as path_split
from subprocess import Popen, PIPE, STDOUT
from os.path import abspath, dirname, join, basename, splitext, exists

EXIT_STATUS = 0
CMD = ''

# obviously this was taken from QIIME but I don't want this module to depend on QIIME
def qiime_system_call(cmd, shell=True):
    """Call cmd and return (stdout, stderr, return_value).

    cmd can be either a string containing the command to be run, or a sequence
    of strings that are the tokens of the command.

    Please see Python's subprocess.Popen for a description of the shell
    parameter and how cmd is interpreted differently based on its value.
    """
    proc = Popen(cmd, shell=shell, universal_newlines=True, stdout=PIPE,
        stderr=PIPE)
    # communicate pulls all stdout/stderr from the PIPEs to 
    # avoid blocking -- don't remove this line!
    stdout, stderr = proc.communicate()
    return_value = proc.returncode
    return stdout, stderr, return_value


# ghetto argument parsing
if len(argv) == 1:
    print 'Not running any tests'
    exit(0)

if len(argv) == 2:
    module_name = argv[1]
    print 'Trying to test %s ...' % module_name

    full_path = abspath(module_name)

    test_path = join(dirname(dirname(full_path)), 'tests')

    if exists(test_path):
        if basename(dirname(full_path)) == 'scripts':
            print 'Running script usage test ...'
            script_call = join(test_path, 'all_tests.py')
            script_name = splitext(module_name)[0]
            CMD = 'source ~/.bash_profile > /dev/null; python %s --suppress_unit_tests --script_usage_tests %s' % (script_call, script_name)
        if basename(dirname(full_path)) in ['test', 'tests']:
            print 'Running test case ...'
            CMD = 'source ~/.bash_profile > /dev/null; python %s' % full_path
        elif exists(join(test_path, 'test_%s' % module_name)):
            print 'Running unit tests ...'
            test_name = join(test_path, 'test_%s' % module_name)
            CMD = 'source ~/.bash_profile > /dev/null; python %s' % test_name
        else:
            print 'This module has no tests to be executed ...'
            exit(1)

        o, e, r = qiime_system_call(CMD)

        print o
        print e
        EXIT_STATUS = r
    else:
        print 'No unit testing? Good luck working as a puke cleaner ... '
        EXIT_STATUS = 1


exit(EXIT_STATUS)
