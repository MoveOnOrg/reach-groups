import pytest
from _pytest.monkeypatch import MonkeyPatch

from update_status_groups import update_status_groups


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class Test():
    monkeypatch = MonkeyPatch()
    existing_groups = []

    # Mock API request for token.
    def mock_get_token(self, args):
        return 'mock token'

    # Mock API request for groups.
    def mock_get_groups(self, args):
        return {'user_groups': self.existing_groups}

    # Mock query results for members by state.
    def mock_get_psql_results(self, args):
        return [{'state': 'CO', 'member_ids': 'mock,member,ids'}]

    # Mock API request to update group.
    def mock_update_group(self, args):
        return {'name': 'updated %s' % args.GROUP_ID, 'member_ids': args.MEMBER_IDS}

    # Mock API request to create group.
    def mock_create_group(self, args):
        return {'name': 'created %s' % args.GROUP_NAME, 'member_ids': args.MEMBER_IDS}

    def test_update_status_groups(self):
        Test.monkeypatch.setattr("update_status_groups.get_token", self.mock_get_token)
        Test.monkeypatch.setattr("update_status_groups.get_groups", self.mock_get_groups)
        Test.monkeypatch.setattr("update_status_groups.get_psql_results", self.mock_get_psql_results)
        Test.monkeypatch.setattr("update_status_groups.update_group", self.mock_update_group)
        Test.monkeypatch.setattr("update_status_groups.create_group", self.mock_create_group)

        # All args are mocked, but still required.
        args = {
            'DB_HOST': 'mock',
            'DB_PORT': 'mock',
            'DB_USER': 'mock',
            'DB_PASS': 'mock',
            'DB_NAME': 'mock',
            'REACH_API_USER': 'mock',
            'REACH_API_PASS': 'mock',
            'STATUS_NAME': 'mock',
            'DB_QUERY': 'mock'
        }
        args = Struct(**args)
        # Test create.
        self.existing_groups = []
        result = update_status_groups(args)
        assert result == {
            'created': [
                {'name': 'created CO: mock', 'member_ids': 'mock,member,ids'}
            ],
            'updated': []
        }
        # Test update.
        self.existing_groups = [{'name': 'CO: mock', 'id': 'existing-group-id'}]
        result = update_status_groups(args)
        assert result == {
            'created': [],
            'updated': [
                {'name': 'updated existing-group-id', 'member_ids': 'mock,member,ids'}
            ]
        }
