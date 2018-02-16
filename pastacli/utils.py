import os
import sys
import click
import requests
from urllib.parse import urlencode

BASE_URL = 'https://pasta.lternet.edu'
CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.pastacli')
AUTH_FILE = os.path.join(CONFIG_DIR, '.auth')

################################################################################
# UTILITIES
################################################################################

def make_url(*parts, query={}):
    url = "/".join([p.strip('/') for p in [BASE_URL] + list(parts)])
    if query:
        url = "{}?{}".format(url, urlencode(query))
    return url


def get(url):
    try:
        res = requests.get(url)
    except requests.exceptions.RequestException:
        print("Failed retrieving {}".format(url)) >> sys.stderr
        sys.exit(1)
    return res


def post(url, **opts):
    try:
        res = requests.post(url, **opts)
    except requests.exceptions.RequestException:
        print("Failed retrieving {}".format(url)) >> sys.stderr
        sys.exit(1)
    return res


def status_check(res, expected=[]):
    if (expected and (res.status_code not in expected)):
        try:
            res.raise_for_status()
            # if it doesn't raise an error, but still isn't the expected
            # response code
            click.echo("Code {} received and not expected".format(
                res.status_code))
            sys.exit()
        except requests.exceptions.HTTPError as e:
            click.echo(e)