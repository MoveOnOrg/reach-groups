# Reach groups - Decommissioned as of 8/16/22

These Python 3.6 scripts create and update Reach.vote user groups to facilitate sending notifications to Reach users based on various status-state combinations, e.g. everyone with unregistered voter contacts in Florida.

# Install

Run `pip install -r requirements.txt` to get requirements to run the code locally, and `pip install -r dev_requirements.txt` to get requirements for running tests (Pytest) and deploying code (Zappa). Copy `settings.py.template` to `settings.py` and fill in any credentials you don't want to pass as command line arguments.

# Add new statuses

To add a new status, just add the relevant query to a SQL file and then add both the status name and the query as paramaters on a new CloudWatch event. See `zappa_settings.yml.template` for event structure.

# Individual scripts

* *get_token.py*: gets a temporary auth token, needed for all the other scripts, though most scripts will get this automatically if given username/password instead of token.
* *create_group.py*: creates a new group.
* *update_group.py*: updates an existing group.
* *delete_group.py*: deletes an existing group.
* *get_groups.py*: gets all the existing groups.
* *update_status_groups.py*: creates or updates a list of groups, one for each state, based on results of a query that returns users by state. `has_voters.sql` is an example query.
* *update_national_group.py*: creates or updates a single group, based on results of a query that returns users. `no_voters.sql` is an example query.
