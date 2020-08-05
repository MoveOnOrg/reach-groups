import requests

from pywell.entry_points import run_from_cli

from get_token import get_token


DESCRIPTION = 'Delete a user group.'

ARG_DEFINITIONS = {
    'REACH_API_USER': 'Reach.vote API username.',
    'REACH_API_PASS': 'Reach.vote API password.',
    'REACH_API_TOKEN': 'Reach.vote API token.',
    'GROUP_ID': 'Name of the new group.'
}

REQUIRED_ARGS = ['GROUP_ID']


def update_group(args):
    if not args.REACH_API_TOKEN:
        args.REACH_API_TOKEN = get_token(args)
    result = requests.delete(
        'https://api.reach.vote/api/v1/user_groups/%s' % args.GROUP_ID,
        headers={
            'Authorization': 'Bearer %s' % args.REACH_API_TOKEN,
        }
    )
    return result.text


if __name__ == '__main__':
    run_from_cli(update_group, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
