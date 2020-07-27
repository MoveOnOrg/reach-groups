# Reach groups

These Python 3.6 scripts create and update Reach.vote user groups to facilitate sending notifications to Reach users based on various status-state combinations, e.g. everyone with unregistered voter contacts in Florida.

# Install

Run `pip install -r requirements.txt` to get requirements to run the code locally, and `pip install -r dev_requirements.txt` to get requirements for running tests (Pytest) and deploying code (Zappa). Copy `settings.py.template` to `settings.py` and fill in any credentials you don't want to pass as command line arguments.

# Add new statuses

To add a new status, just add the relevant query to a SQL file and then add both the status name and the query as paramaters on a new CloudWatch event. See `zappa_settings.yml.template` for event structure.
