import libuser
import secrets
import hashlib
import tempfile
import os

from pathlib import Path


def keygen(username, password=None):

    if password:
        if not libuser.login(username, password):
            return None

    # FIXED B311: Use secrets module instead of random for cryptographic purposes
    key = hashlib.sha256(str(secrets.randbits(2048)).encode()).hexdigest()

    # FIXED B108: Use secure temp directory instead of hardcoded /tmp/
    tmpdir = tempfile.gettempdir()
    for f in Path(tmpdir).glob('vulpy.apikey.' + username + '.*'):
        print('removing', f)
        f.unlink()

    keyfile = os.path.join(tmpdir, 'vulpy.apikey.{}.{}'.format(username, key))

    Path(keyfile).touch()

    return key


def authenticate(request):
    if 'X-APIKEY' not in request.headers:
        return None

    key = request.headers['X-APIKEY']

    # FIXED B108: Use secure temp directory
    tmpdir = tempfile.gettempdir()
    for f in Path(tmpdir).glob('vulpy.apikey.*.' + key):
        return f.name.split('.')[2]

    return None

