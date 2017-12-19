import json
import re
import os
import urllib


def is_slackbot(agent):
    slack_agents = [
        r'Slackbot\-LinkExpanding .*'
    ]
    for a in slack_agents:
        if re.match(a, agent):
            return True
    return False


def redirect(url):
    return ok(
        body='',
        headers={'Location': url},
        code=307
    )


def slack_response(dest):
    metadata = '''
    <html>
    <head>
        <meta property="og:type" content="website" />
        <meta property="og:url" content="{}" />
        <meta property="og:title" content="{}" />
        <meta property="og:description" content="{}" />
        <meta property="og:image" content="{}" />
    </head>
    </html'''.format(
        dest,
        'NSFL/W Proxy',
        'The contents of this URL could be NSFW/NSFL',
        os.getenv('NSFW_IMAGE_URL'))
    return ok(body=metadata)


def ok(body='', headers=None, code=200):
    ret = {
        "statusCode": code,
        "body": body
    }
    if headers is not None:
        ret['headers'] = headers
    print ret
    return ret


def index(event, context):
    if event['path'] == '/favicon.ico':
        return ok()

    dest = urllib.unquote(event['path'][1:]).decode('utf8')
    if 'User-Agent' in event['headers']:
        if is_slackbot(event['headers']['User-Agent']):
            return slack_response(dest)
    return redirect(dest)

    return ok(body='No user agent set')
