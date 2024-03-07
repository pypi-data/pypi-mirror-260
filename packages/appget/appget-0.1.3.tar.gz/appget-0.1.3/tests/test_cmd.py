import os

from appget.cmd import run, runs

CURRENT_FILE = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_FILE)
PARENT_DIR = os.path.abspath(CURRENT_DIR + "/..")


def test_run():
    print('\ntest_run: start')

    ret = run('pwd')
    assert ret.returncode == 0
    assert len(ret.stdout) > 0
    assert ret.stdout.replace('\n', '') == CURRENT_DIR

    ret = run('echo $SHELL')
    assert ret.returncode == 0
    assert len(ret.stdout) > 0

    ret = run('ls -lah ..')
    assert ret.returncode == 0
    assert len(ret.stdout) > 0

    ret = run(['ls', '-lah', '..'], shell=False)
    assert ret.returncode == 0
    assert len(ret.stdout) > 0

    print('test_run: end')


def test_runs():
    print('\ntest_runs: start')

    rets = runs('pwd', 'date', 'ls .')
    assert all(ret.returncode == 0 for ret in rets)
    assert all(len(ret.stdout) > 0 for ret in rets)

    rets = runs(['pwd', 'date', 'ls .'])
    assert all(ret.returncode == 0 for ret in rets)
    assert all(len(ret.stdout) > 0 for ret in rets)

    print('test_runs: end')
