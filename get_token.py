import requests

from pywell.entry_points import run_from_cli


DESCRIPTION = 'Get API token.'

ARG_DEFINITIONS = {
    'REACH_API_USER': 'Reach.vote API username.',
    'REACH_API_PASS': 'Reach.vote API password.'
}

REQUIRED_ARGS = [
    'REACH_API_USER', 'REACH_API_PASS'
]


def get_token(args):
    result = requests.post(
        'https://api.reach.vote/oauth/token',
        data={
            'username': args.REACH_API_USER,
            'password': args.REACH_API_PASS
        }
    )
    if result.status_code != 200:
        return 'Error: %s %s' % (result.status_code, result.json().get('detail', '(no error detail)'))
    return result.json().get('access_token')


if __name__ == '__main__':
    run_from_cli(get_token, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
