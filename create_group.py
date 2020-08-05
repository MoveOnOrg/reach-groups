import requests

from pywell.entry_points import run_from_cli

from get_token import get_token


DESCRIPTION = 'Create a user group.'

ARG_DEFINITIONS = {
    'REACH_API_USER': 'Reach.vote API username.',
    'REACH_API_PASS': 'Reach.vote API password.',
    'REACH_API_TOKEN': 'Reach.vote API token.',
    'CREATOR_ID': 'User ID for group creator.',
    'GROUP_NAME': 'Name of the new group.',
    'MEMBER_IDS': 'Comma-separated user IDs for initial group members.'
}

REQUIRED_ARGS = ['GROUP_NAME']


def create_group(args):
    if not args.REACH_API_TOKEN:
        args.REACH_API_TOKEN = get_token(args)
    json = {
        'name': args.GROUP_NAME,
        'display_name': args.GROUP_NAME
    }
    if 'CREATOR_ID' in args and args.CREATOR_ID:
        json['created_by_user_id'] = args.CREATOR_ID
    if 'MEMBER_IDS' in args and args.MEMBER_IDS:
        member_ids = args.MEMBER_IDS.split(',')
        json['users'] = [{'user_id': member_id} for member_id in member_ids]
    result = requests.post(
        'https://api.reach.vote/api/v1/user_groups',
        headers={
            'Authorization': 'Bearer %s' % args.REACH_API_TOKEN,
        },
        json=json
    )
    if result.status_code != 201:
        return 'Error: %s %s' % (result.status_code, result.json().get('detail', '(no error detail)'))
    return result.json()


if __name__ == '__main__':
    run_from_cli(create_group, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
