import requests

from pywell.entry_points import run_from_cli

from get_token import get_token


DESCRIPTION = 'Get user groups.'

ARG_DEFINITIONS = {
    'REACH_API_USER': 'Reach.vote API username.',
    'REACH_API_PASS': 'Reach.vote API password.',
    'REACH_API_TOKEN': 'Reach.vote API token.'
}

REQUIRED_ARGS = []


def get_groups(args):
    if not args.REACH_API_TOKEN:
        args.REACH_API_TOKEN = get_token(args)
    result = requests.get(
        'https://api.reach.vote/api/v1/user_groups',
        headers={
            'Authorization': 'Bearer %s' % args.REACH_API_TOKEN,
        }
    )
    if result.status_code == 404:
        return {'user_groups': []}
    if result.status_code != 200:
        return 'Error: %s %s' % (result.status_code, result.json().get('detail', '(no error detail)'))
    return result.json()


if __name__ == '__main__':
    run_from_cli(get_groups, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
