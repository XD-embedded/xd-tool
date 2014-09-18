import xd.tool.shell

from nose.tools import raises, with_setup

import os
import tempfile
import glob

def setup():
    global testdir, testcwd
    testcwd = os.getcwd()
    testdir = tempfile.mkdtemp(prefix='nose-')

def teardown():
    os.chdir(testcwd)
    os.rmdir(testdir)

def setup_chdir():
    os.chdir(testcwd)

def teardown_chdir():
    os.chdir(testcwd)

def setup_call():
    os.chdir(testdir)

def teardown_call():
    os.chdir(testdir)
    for f in glob.glob(os.path.join(testdir, '*')):
        os.unlink(f)


@with_setup(setup_chdir, teardown_chdir)
def test_chdir():
    assert os.getcwd() != testdir
    xd.tool.shell.chdir(testdir)
    assert os.getcwd() == testdir

@with_setup(setup_chdir, teardown_chdir)
def test_chdir_quiet():
    assert os.getcwd() != testdir
    xd.tool.shell.chdir(testdir, quiet=True)
    assert os.getcwd() == testdir

@with_setup(setup_chdir, teardown_chdir)
@raises(OSError)
def test_chdir_nonexistant():
    assert not os.path.exists('/tmp/THIS_DIRECTORY_SHOULD_NOT_EXIST')
    xd.tool.shell.chdir('/tmp/THIS_DIRECTORY_SHOULD_NOT_EXIST')

@with_setup(setup_chdir, teardown_chdir)
def test_chdir_nonexistant_cwd():
    cwd = tempfile.mkdtemp(prefix='nose-')
    os.chdir(cwd)
    os.rmdir(cwd)
    xd.tool.shell.chdir(testdir)
    assert os.getcwd() == testdir

@with_setup(setup_chdir, teardown_chdir)
def test_chdir_same():
    os.chdir(testdir)
    xd.tool.shell.chdir(testdir)
    assert os.getcwd() == testdir


@with_setup(setup_chdir, teardown_chdir)
def test_pushd_popd():
    xd.tool.shell.pushd(testdir)
    assert os.getcwd() == testdir
    xd.tool.shell.popd()
    assert os.getcwd() == testcwd


@with_setup(setup_call, teardown_call)
def test_call():
    assert not os.path.exists("FOOBAR")
    xd.tool.shell.call("touch FOOBAR")
    assert os.path.exists("FOOBAR")

@with_setup(setup_call, teardown_call)
def test_call_quiet():
    assert not os.path.exists("FOOBAR")
    xd.tool.shell.call("touch FOOBAR", quiet=True)
    assert os.path.exists("FOOBAR")

@with_setup(setup_call, teardown_call)
def test_call_path():
    os.chdir(testcwd)
    assert not os.path.exists(os.path.join(testdir, "FOOBAR"))
    xd.tool.shell.call("touch FOOBAR", testdir)
    assert os.path.exists(os.path.join(testdir, "FOOBAR"))

@with_setup(setup_call, teardown_call)
def test_call_path_nonexistant():
    baddir = '/tmp/THIS_DIRECTORY_SHOULD_NOT_EXIST'
    assert not os.path.exists(baddir)
    assert xd.tool.shell.call("touch %s/FOOBAR"%(testdir), baddir) is None
    assert not os.path.exists(os.path.join(testdir, "FOOBAR"))

@with_setup(setup_call, teardown_call)
def test_call_true():
    assert xd.tool.shell.call("true") == True

@with_setup(setup_call, teardown_call)
def test_call_false():
    assert xd.tool.shell.call("false") is None

@with_setup(setup_call, teardown_call)
def test_call_quiet_output():
    output = xd.tool.shell.call("echo foobar", quiet=True)
    assert output.decode('utf-8') == 'foobar\n'

@with_setup(setup_call, teardown_call)
def test_call_quiet_output_true():
    output = xd.tool.shell.call("true", quiet=True)
    assert output.decode('utf-8') == ''

@with_setup(setup_call, teardown_call)
def test_call_quiet_output_false():
    output = xd.tool.shell.call("false", quiet=True)
    assert output is None
