import json
import base64
import logging

logger = logging.getLogger(__name__)

def create(response, username):
    session = base64.b64encode(json.dumps({'username': username}).encode())
    response.set_cookie('vulpy_session', session)
    return response


def load(request):

    session = {}
    cookie = request.cookies.get('vulpy_session')

    try:
        if cookie:
            decoded = base64.b64decode(cookie.encode())
            if decoded:
                session = json.loads(base64.b64decode(cookie))
    except Exception as e:
        # FIXED B110: Log exception instead of silently passing
        logger.warning(f"Failed to load session cookie: {e}")
        pass

    return session


def destroy(response):
    response.set_cookie('vulpy_session', '', expires=0)
    return response

