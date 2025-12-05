from pathlib import Path
import tempfile
import os

import click
import requests

# FIXED B108: Use secure temp directory instead of hardcoded /tmp/
api_key_file = Path(os.path.join(tempfile.gettempdir(), 'supersecret.txt'))

@click.command()
@click.argument('message')
def cmd_api_client(message):
    if not api_key_file.exists():

        username = click.prompt('Username')
        password = click.prompt('Password', hide_input=True)

        # FIXED B113: Added timeout to prevent hanging requests
        r = requests.post('http://127.0.1.1:5000/api/key', json={'username':username, 'password':password}, timeout=10)

        if r.status_code != 200:
            click.echo('Invalid authentication or other error ocurred. Status code: {}'.format(r.status_code))
            return False


        api_key = r.json()['key']
        print('Received key:', api_key)

        with api_key_file.open('w') as outfile:
            outfile.write(api_key)

    api_key = api_key_file.open().read()
    # FIXED B113: Added timeout to prevent hanging requests
    r = requests.post('http://127.0.1.1:5000/api/post', json={'text':message}, headers={'X-APIKEY': api_key}, timeout=10)
    print(r.text)


if __name__ == '__main__':
    cmd_api_client()
