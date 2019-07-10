import boto3
import logging
import os
import sys


ENVIRONMENT_DEFAULTS = {
    'EA ORE': {
        'label': 'ea',
        'elb_url': 'lb-ea-ore.starfishsolutions.com',
        'tenant_db': {
            'rds_id': 'sf-rds-ea-single-tenant-dbs02-ore',
            'rds_replica_id': 'sf-rds-ea-single-tenant-dbs02-ore'
        },
        'sfadmin_db': {
            'name': 'sfadmin_ea_ore',
            'host': 'sfadmin-ea-ore.db.starfishsolutions.com'
        },
        'success_network': {
            'api_name': 'SERVICE_API_SSN_EA_ORE',
            'endpoint': 'https://blaise-api.hesos.net/sf-success-network-ea/tenants/{tenant_id}/users/{user_id}/'
        },
        'appointments': {
            'api_name': 'SERVICE_API_APPTS_EA_ORE',
            'endpoint': 'https://blaise-api.hesos.net/sf-appts-ea/tenants/{tenant_id}/users/{user_id}/'
        },
        'saved_filters': {
            'api_name': 'SERVICE_API_SSF_EA_ORE',
            'endpoint': 'https://blaise-api.hesos.net/sf-saved-filters-ea-ore/tenants/{tenant_id}/users/{user_id}/'
        }
    },
    'OPS ORE': {
        'label': 'ops',
        'elb_url': 'lb-ops-ore.starfishsolutions.com',
        'tenant_db': {
            'rds_id': 'sf-rds-ops-single-tenant-dbs03-ore',
            'rds_replica_id': 'sf-rds-ops-single-tenant-dbs03-ore'
        },
        'sfadmin_db': {
            'name': 'sfadmin_ops_ore',
            'host': 'sfadmin-ops-ore.db.starfishsolutions.com'
        },
        'success_network': {
            'api_name': 'SERVICE_API_SSN_OPS_ORE',
            'endpoint': 'https://blaise-api.hesos.net/sf-success-network-ops/tenants/{tenant_id}/users/{user_id}/'
        },
        'appointments': {
            'api_name': 'SERVICE_API_APPTS_OPS_ORE',
            'endpoint': 'https://blaise-api.hesos.net/sf-appts-ops/tenants/{tenant_id}/users/{user_id}/'
        },
        'saved_filters': {
            'api_name': 'SERVICE_API_SSF_OPS_ORE',
            'endpoint': 'https://blaise-api.hesos.net/sf-saved-filters-ops-ore/tenants/{tenant_id}/users/{user_id}/'
        }
    }
}


class SFTenantEnvironment:
    """Holds all environment variables and their defaults."""
    required_configs = {
        'branch': 'Starfish branch name used to source DB refresh scripts',
        'subdomain': 'Tenant subdomain (subdomain.starfishsolutions.com)',
        'db_name': 'Name of the DB for this single-tenant schema',
        'postgres_user': 'Username for logging into postgres',
        'sfadmin_db_hostname': 'DNS of the SFAdmin DB',
        'sfadmin_db_name': 'Name of the SFAdmin DB',
        'elb_url': 'ELB that the tenant DNS will point to',
        'rds_id': 'RDS instance that houses the single-tenant schemas',
        'rds_replica_id': 'RDS read replica instance that houses the single-tenant schemas',
        'starfish_release_host': 'The host in the starfish-release project in which DB confs will be stored',
        'workmail_username': 'Workmail user name',
        'workmail_display_name': 'Workmail User displayname',
        'workmail_password': 'Workmail account password',
        'workmail_organization_id': 'Organization ID value for workmail',
        'host_zone_id': 'Host_Zone_ID for route53'
    }

    def __init__(self):
        if self.rds_id and self.rds_replica_id:
            self.db_hostname = self.rds_endpoint_address(self.rds_id)
            self.replica_db_hostname = self.rds_endpoint_address(self.rds_replica_id)

        self.validate_env_vars()

    @property
    def environment(self) -> dict:
        return ENVIRONMENT_DEFAULTS.get(os.environ.get('ENVIRONMENT', ''), {})

    @property
    def branch(self) -> str:
        return os.environ.get('BRANCH', '')

    @property
    def subdomain(self) -> str:
        return os.environ.get('SUBDOMAIN', '')

    @property
    def postgres_user(self) -> str:
        return os.environ.get('POSTGRES_USER', '')

    @property
    def postgres_password(self) -> str:
        return os.environ.get('POSTGRES_PASSWORD', '')

    @property
    def base_db_name(self) -> str:
        return os.environ.get('BASE_DB_NAME', 'postgres')

    @property
    def db_name(self) -> str:
        return os.environ.get('DB_NAME', '')

    @property
    def starfish_release_host(self) -> str:
        return os.environ.get('STARFISH_RELEASE_HOST', '')

    @property
    def sfadmin_db_hostname(self) -> str:
        return os.environ.get('SFADMIN_DB_HOSTNAME',
            self.environment['sfadmin_db']['host'] if self.environment else '')

    @property
    def sfadmin_db_name(self) -> str:
        return os.environ.get('SFADMIN_DB_NAME',
            self.environment['sfadmin_db']['name'] if self.environment else '')

    @property
    def elb_url(self) -> str:
        return os.environ.get('ELB_URL',
            self.environment['elb_url'] if self.environment else '')

    @property
    def rds_id(self) -> str:
        return os.environ.get('RDS_ID',
            self.environment['tenant_db']['rds_id'] if self.environment else '')

    @property
    def rds_replica_id(self) -> str:
        return os.environ.get('RDS_REPLICA_ID',
            self.environment['tenant_db']['rds_replica_id'] if self.environment else '')

    @property
    def service_api_success_network_endpoint(self) -> str:
        return os.environ.get('SERVICE_API_SUCCESS_NETWORK_ENDPOINT',
            self.environment['success_network']['endpoint'] if self.environment else '')

    @property
    def service_api_success_network_key(self) -> str:
        return os.environ.get('SERVICE_API_SUCCESS_NETWORK_KEY',
            os.environ.get(self.environment['success_network']['api_name'] if self.environment else '', ''))

    @property
    def service_api_appointments_endpoint(self) -> str:
        return os.environ.get('SERVICE_API_APPOINTMENTS_ENDPOINT',
            self.environment['appointments']['endpoint'] if self.environment else '')

    @property
    def service_api_appointments_key(self) -> str:
        return os.environ.get('SERVICE_API_APPOINTMENTS_KEY',
            os.environ.get(self.environment['appointments']['api_name'] if self.environment else '', ''))

    @property
    def service_api_saved_filters_endpoint(self) -> str:
        return os.environ.get('SERVICE_API_SAVED_FILTERS_ENDPOINT',
            self.environment['saved_filters']['endpoint'] if self.environment else '')

    @property
    def service_api_saved_filters_key(self) -> str:
        return os.environ.get('SERVICE_API_SAVED_FILTERS_KEY',
            os.environ.get(self.environment['saved_filters']['api_name'] if self.environment else '', ''))

    @property
    def mobile_surveys_enabled(self) -> str:
        return os.environ.get('MOBILE_SURVEYS_ENABLED',
            'true' if self.environment and self.environment['label'] == 'ea' else 'false')

    @property
    def responsive_kiosk_enabled(self) -> str:
        return os.environ.get('RESPONSIVE_KIOSK_ENABLED',
            'true' if self.environment and self.environment['label'] == 'ea' else 'false')

    @property
    def note(self) -> str:
        return os.environ.get('TENANT_CREATE_NOTE', '')

    @property
    def starfish_db_script_dir(self) -> str:
        return '{workspace}/starfish-all/web/def/scripts/refresh/'.format(workspace=os.environ.get('WORKSPACE'))

    @property
    def workmail_username(self) -> str:
        return os.environ.get('WORKMAIL_USERNAME', '')

    @property
    def workmail_display_name(self) -> str:
        return os.environ.get('WORKMAIL_DISPLAY_NAME', '')

    @property
    def workmail_password(self) -> str:
        return os.environ.get('WORKMAIL_PASSWORD', '')

    @property
    def workmail_organization_id(self) -> str:
        return os.environ.get('WORKMAIL_ORGANIZATION_ID', '')

    @property
    def host_zone_id(self) -> str:
        return os.environ.get('HOST_ZONE_ID', '')

    @staticmethod
    def rds_endpoint_address(rds_id: str = '') -> str:
        return boto3.client('rds').describe_db_instances(
                DBInstanceIdentifier=rds_id
            ).DBInstances[0].Endpoint.Address if rds_id else ''

    def validate_env_vars(self) -> None:
        """Validates and prints info about environment variables"""
        if not self.environment:
            logging.warning('No environment input, falling back to set parameters.')

        missing_configs = [config for config in self.required_configs if not getattr(self, config, None)]

        if missing_configs:
            for config in missing_configs:
                logging.critical(config.upper(), ' missing.')
                logging.critical(config.upper(), ': ', self.required_configs[config])
            raise Exception('Missing required variables. Provide appropriate environment variables.')

        for config in self.required_configs:
            logging.info(config, ': ', getattr(self, config, None))
