import pytest


@pytest.fixture
def ea_minimum_environment_variables() -> dict:
    return {'ENVIRONMENT': 'EA ORE',
            'BRANCH': 'testbranch',
            'SUBDOMAIN': 'test',
            'DB_NAME': 'test_db',
            'POSTGRES_USER': 'test_pg_user',
            'STARFISH_RELEASE_HOST': 'hostname',
            'WORKSPACE': 'test/sql',
            'WORKMAIL_USERNAME': 'test_workmail_username',
            'WORKMAIL_DISPLAY_NAME': 'test_workmail_display_name',
            'WORKMAIL_PASSWORD': 'test_workmail_password',
            'WORKMAIL_ORGANIZATION_ID': 'test_organization_id',
            'HOST_ZONE_ID': 'test_host_zone_id'}


@pytest.fixture
def ops_minimum_environment_variables() -> dict:
    return {'ENVIRONMENT': 'OPS ORE',
            'BRANCH': 'testbranch',
            'SUBDOMAIN': 'test',
            'DB_NAME': 'test_db',
            'POSTGRES_USER': 'test_pg_user',
            'STARFISH_RELEASE_HOST': 'hostname',
            'WORKSPACE': 'test/sql',
            'WORKMAIL_USERNAME': 'test_workmail_username',
            'WORKMAIL_DISPLAY_NAME': 'test_workmail_display_name',
            'WORKMAIL_PASSWORD': 'test_workmail_password',
            'WORKMAIL_ORGANIZATION_ID': 'test_organization_id',
            'HOST_ZONE_ID': 'test_host_zone_id'}


@pytest.fixture
def custom_environment_variables() -> dict:
    return {'BRANCH': 'testbranch',
            'SUBDOMAIN': 'test',
            'DB_NAME': 'test_db',
            'POSTGRES_USER': 'test_pg_user',
            'POSTGRES_PASSWORD': 'test_pg_password',
            'BASE_DB_NAME': 'test_base_db',
            'STARFISH_RELEASE_HOST': 'hostname',
            'SFADMIN_DB_HOSTNAME': 'test_sfadmin_db_host',
            'SFADMIN_DB_NAME': 'test_sfadmin_db_name',
            'ELB_URL': 'test_elb_url',
            'RDS_ID': 'test_rds_id',
            'RDS_REPLICA_ID': 'test_rds_replica_id',
            'SERVICE_API_SUCCESS_NETWORK_ENDPOINT': 'test_ssn_endpoint',
            'SERVICE_API_SUCCESS_NETWORK_KEY': 'test_ssn_key',
            'SERVICE_API_APPOINTMENTS_ENDPOINT': 'test_appts_endpoint',
            'SERVICE_API_APPOINTMENTS_KEY': 'test_appts_key',
            'SERVICE_API_SAVED_FILTERS_ENDPOINT': 'test_ssf_endpoint',
            'SERVICE_API_SAVED_FILTERS_KEY': 'test_ssf_key',
            'MOBILE_SURVEYS_ENABLED': 'test_mobile_surveys_enabled',
            'RESPONSIVE_KIOSK_ENABLED': 'test_responsive_kiosk_enabled',
            'TENANT_CREATE_NOTE': 'test note',
            'WORKSPACE': 'tests/sql',
            'WORKMAIL_USERNAME': 'test_workmail_username',
            'WORKMAIL_DISPLAY_NAME': 'test_workmail_display_name',
            'WORKMAIL_PASSWORD': 'test_workmail_password',
            'WORKMAIL_ORGANIZATION_ID': 'test_organization_id',
            'HOST_ZONE_ID': 'test_host_zone_id'
            }
