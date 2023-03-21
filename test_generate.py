import capture
import sys
import os

def test_generate(tmpdir):
    print(tmpdir)
    root = os.path.dirname(os.path.abspath(__file__))

    os.environ['OSBO_CACHE'] = os.path.join(tmpdir, 'cache')
    os.environ['OSBO_SITE'] = os.path.join(tmpdir, 'site')
    # os.environ['OSBO_ORG'] = os.path.join(tmpdir, 'organisations')
    os.environ['OSBO_GITHUB'] = os.path.join(root, 'tests', 'data', 'github')
    token = os.environ['MY_GITHUB_TOKEN']
    os.environ['MY_GITHUB_TOKEN'] = ''
    exit_code, out, err = capture.separated([sys.executable, 'generate.py'])
    print(out)
    assert err == ''
    assert exit_code == 0

    os.environ['MY_GITHUB_TOKEN'] = token
    exit_code, out, err = capture.separated([sys.executable, 'generate.py'])
    print(out)
    assert err == ''
    assert exit_code == 0
