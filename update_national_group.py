import requests

from pywell.entry_points import run_from_cli, run_from_lamba
from pywell.get_psql_results import get_psql_results

from get_token import get_token
from get_groups import get_groups
from create_group import create_group
from update_group import update_group


DESCRIPTION = 'Update membership for all groups associated with a status.'

ARG_DEFINITIONS = {
    'DB_HOST': 'Database host IP or hostname.',
    'DB_PORT': 'Database port number.',
    'DB_USER': 'Database user.',
    'DB_PASS': 'Database password.',
    'DB_NAME': 'Database name.',
    'REACH_API_USER': 'Reach.vote API username.',
    'REACH_API_PASS': 'Reach.vote API password.',
    'STATUS_NAME': 'Name of status group.',
    'DB_QUERY': 'Raw query or path to .sql file, should return a comma-separated member_ids column.'
}

REQUIRED_ARGS = [
    'DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASS', 'DB_NAME',
    'REACH_API_USER', 'REACH_API_PASS', 'STATUS_NAME', 'DB_QUERY'
]


def update_national_status_group(args):
    updated = []
    created = []
    # Get all the data.
    args.REACH_API_TOKEN = get_token(args)
    groups = get_groups(args).get('user_groups', [])
    args.MEMBER_IDS = get_psql_results(args)[0].get('member_ids', '')
    args.GROUP_NAME = args.STATUS_NAME
    # Check if group exists already, by matching name.
    matching_groups = [group for group in groups if group.get('name') == args.GROUP_NAME]
    if len(matching_groups):
        args.GROUP_ID = matching_groups[0].get('id', '')
        # Compare the member lists to see if update is needed.
        old_member_ids = [user.get('user_id', '') for user in matching_groups[0].get('users', [])]
        new_member_ids = args.MEMBER_IDS.split(',')
        old_member_ids.sort()
        new_member_ids.sort()
        if old_member_ids != new_member_ids:
            updated.append(update_group(args))
    else:
        created.append(create_group(args))
    return {
        'created': created,
        'updated': updated
    }


def aws_lambda(event, context):
    return run_from_lamba(update_national_status_group, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS, event)


if __name__ == '__main__':
    run_from_cli(update_national_status_group, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
