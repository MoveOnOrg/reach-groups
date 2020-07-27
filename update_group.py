import requests

from pywell.entry_points import run_from_cli

from get_token import get_token


DESCRIPTION = 'Update a user group members.'

ARG_DEFINITIONS = {
    'REACH_API_USER': 'Reach.vote API username.',
    'REACH_API_PASS': 'Reach.vote API password.',
    'REACH_API_TOKEN': 'Reach.vote API token.',
    'GROUP_ID': 'Name of the new group.',
    'MEMBER_IDS': 'Comma-separated user IDs for initial group members.'
}

REQUIRED_ARGS = [
    'GROUP_ID',
    'MEMBER_IDS'
]


def update_group(args):
    if not args.REACH_API_TOKEN:
        args.REACH_API_TOKEN = get_token(args)
    member_ids = args.MEMBER_IDS.split(',')
    json = {
        'users': [{'user_id': member_id} for member_id in member_ids]
    }
    result = requests.put(
        'https://api.reach.vote/api/v1/user_groups/%s' % args.GROUP_ID,
        headers={
            'Authorization': 'Bearer %s' % args.REACH_API_TOKEN,
        },
        json=json
    )
    if result.status_code != 200:
        return 'Error: %s %s' % (result.status_code, result.json().get('detail', '(no error detail)'))
    return result.json()


if __name__ == '__main__':
    run_from_cli(update_group, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
