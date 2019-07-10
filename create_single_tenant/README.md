# Create Single Tenant

This Python package creates a new Starfish tenant based on environment variables.

## Installation

Create and activate a Python 3 virtual environment.

```bash
python3 -m venv /path/to/new/virtual/environment
source /path/to/new/virtual/environment/bin/activate
```

Then install dependencies in your active virtualenv.

```bash
pip install -r requirements.txt
```

## Usage

You can call create_single_tenant from its parent directory with the virtual
environment active:

```bash
python create_single_tenant
```

### Environment Variables

Create Single Tenant uses the following environment variables:

- BRANCH
  - Starfish branch name used to source DB refresh scripts
  - This must match the branch specified for Starfish in this job
- SUBDOMAIN
  - Tenant subdomain
- DB_NAME
  - Name of the DB for this single-tenant schema
- POSTGRES_USER
  - Username for logging into postgres
- POSTGRES_PASSWORD
  - Password for logging into postgres _(can be blank)_
- BASE_DB_NAME
  - _optional_ Name of database to create tenant db from _(Default is_ `postgres`_)_
- STARFISH_RELEASE_HOST
  - The host in the starfish-release project in which DB confs will be stored
- WORKMAIL_USERNAME
  - The 'user-id' part of email-id which will be created (ex., user-id@domain.com)
- WORKMAIL_DISPLAY_NAME
  - Workmail Users display name
- WORKMAIL_PASSWORD
  - Workmail accounts password
- WORKMAIL_ORGANIZATION_ID
  - Organization ID value for workmail
- HOSTZONE_ID
	- HostZoneID value for Route53 domain
- TENANT_CREATE_NOTE
  - A note to be left in the newly created database (ex., Config set by Jenkins job `${JOB_NAME} (${JOB_ID}`)
- ENVIRONMENT
  - Choices:
    1. EA ORE
    2. OPS ORE

If ENVIRONMENT is given, the following default values will be set:

- EA ORE (Test Tenants):
  - SFADMIN_DB_HOSTNAME: sfadmin-ea-ore.db.starfishsolutions.com
  - SFADMIN_DB_NAME: sfadmin_ea_ore
  - ELB_URL: lb-ea-ore.starfishsolutions.com
  - RDS_ID: sf-rds-ea-single-tenant-dbs02-ore
  - RDS_REPLICA_ID: sf-rds-ea-single-tenant-dbs02-ore
  - Default values for SERVICE_API configs (endpoints and keys)
- OPS ORE (Live Tenants):
  - SFADMIN_DB_HOSTNAME: sfadmin-ops-ore.db.starfishsolutions.com
  - SFADMIN_DB_NAME: sfadmin_ops_ore
  - ELB_URL: lb-ops-ore.starfishsolutions.com
  - RDS_ID: sf-rds-ops-single-tenant-dbs03-ore
  - RDS_REPLICA_ID: sf-rds-ops-single-tenant-dbs03-ore
  - Default values for SERVICE_API configs (endpoints and keys)

The environment variables below can be absent unless default settings need to be overridden.

- SFADMIN_DB_HOSTNAME
  - _optional_ DNS of the SFAdmin DB
- SFADMIN_DB_NAME
  - _optional_ Name of the SFAdmin DB
- ELB_URL
  - _optional_ ELB that the tenant DNS will point to
- RDS_ID
  - _optional_ RDS instance that houses the single-tenant schemas
- RDS_REPLICA_ID
  - _optional_ RDS read replica instance that houses the single-tenant schemas
- SERVICE_API_SUCCESS_NETWORK_ENDPOINT
  - _optional_ The endpoint for connecting to the Success Network API
- SERVICE_API_SUCCESS_NETWORK_KEY
  - _optional_ The key for connecting to the Success Network API
- SERVICE_API_APPOINTMENTS_ENDPOINT
  - _optional_ The endpoint for connecting to the Appointments API
- SERVICE_API_APPOINTMENTS_KEY
  - _optional_ The key for connecting to the Appointments API
- MOBILE_SURVEYS_ENABLED
  - _optional_ Enables mobile surveys in the new tenant
- RESPONSIVE_KIOSK_ENABLED
  - _optional_ Enables responsive kiosks in the new tenant
- SERVICE_API_SAVED_FILTERS_ENDPOINT
  - _optional The endpoint for connecting to the Saved Filters API
- SERVICE_API_SAVED_FILTERS_KEY
  - _optional The key for connecting to the Saved Filters API

## Testing

```bash
python -m pytest
```
