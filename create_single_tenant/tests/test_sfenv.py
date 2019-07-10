import pytest

from unittest.mock import patch

from sfenv import SFTenantEnvironment


class TestSFTenantEnvironment:
    def set_environment_vars(self, vars: dict, monkeypatch):
        for key in vars:
            monkeypatch.setenv(key, vars[key])

    @patch('boto3.client')
    def test_validate_env_vars_ea_defaults(self,
                                           client,
                                           ea_minimum_environment_variables,
                                           capsys,
                                           monkeypatch):
        self.set_environment_vars(ea_minimum_environment_variables, monkeypatch)
        SFTenantEnvironment()
        client.assert_called()
        assert 'missing' not in capsys.readouterr().err

    @patch('boto3.client')
    def test_validate_with_custom_environment_variables(self,
                                                        client,
                                                        custom_environment_variables,
                                                        capsys,
                                                        monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        SFTenantEnvironment()
        client.assert_called()
        assert 'missing' not in capsys.readouterr().err

    @patch('boto3.client')
    def test_init_raises_exceptions_without_environment_vars_set(self, client):
        with pytest.raises(Exception, match='Missing required variables.'):
            SFTenantEnvironment()

    @patch('boto3.client')
    def test_environment_ea_defaults(self,
                                     client,
                                     ea_minimum_environment_variables,
                                     monkeypatch):
        self.set_environment_vars(ea_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.environment == {
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
        }

    @patch('boto3.client')
    def test_environment_ops_defaults(self,
                                      client,
                                      ops_minimum_environment_variables,
                                      monkeypatch):
        self.set_environment_vars(ops_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.environment == {
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

    @patch('boto3.client')
    def test_environment_custom_env_vars(self,
                                         client,
                                         custom_environment_variables,
                                         monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.environment == {}

    @patch('boto3.client')
    def test_branch(self,
                    client,
                    custom_environment_variables,
                    monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.branch == 'testbranch'

    @patch('boto3.client')
    def test_subdomain(self,
                       client,
                       custom_environment_variables,
                       monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.subdomain == 'test'

    @patch('boto3.client')
    def test_postgres_user(self,
                       client,
                       custom_environment_variables,
                       monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.postgres_user == 'test_pg_user'

    @patch('boto3.client')
    def test_postgres_password(self,
                       client,
                       custom_environment_variables,
                       monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.postgres_password == 'test_pg_password'

    @patch('boto3.client')
    def test_base_db_name(self,
                       client,
                       custom_environment_variables,
                       monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.base_db_name == 'test_base_db'

    @patch('boto3.client')
    def test_db_name(self,
                     client,
                     custom_environment_variables,
                     monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.db_name == 'test_db'

    @patch('boto3.client')
    def test_starfish_release_host(self,
                                   client,
                                   custom_environment_variables,
                                   monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.starfish_release_host == 'hostname'

    @patch('boto3.client')
    def test_sfadmin_db_hostname(self,
                                 client,
                                 custom_environment_variables,
                                 monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.sfadmin_db_hostname == 'test_sfadmin_db_host'

    @patch('boto3.client')
    def test_sfadmin_db_hostname_ea_default(self,
                                            client,
                                            ea_minimum_environment_variables,
                                            monkeypatch):
        self.set_environment_vars(ea_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.sfadmin_db_hostname == 'sfadmin-ea-ore.db.starfishsolutions.com'

    @patch('boto3.client')
    def test_sfadmin_db_hostname_ops_default(self,
                                             client,
                                             ops_minimum_environment_variables,
                                             monkeypatch):
        self.set_environment_vars(ops_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.sfadmin_db_hostname == 'sfadmin-ops-ore.db.starfishsolutions.com'

    @patch('boto3.client')
    def test_sfadmin_db_name(self,
                             client,
                             custom_environment_variables,
                             monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.sfadmin_db_name == 'test_sfadmin_db_name'

    @patch('boto3.client')
    def test_sfadmin_db_name_ea_default(self,
                                        client,
                                        ea_minimum_environment_variables,
                                        monkeypatch):
        self.set_environment_vars(ea_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.sfadmin_db_name == 'sfadmin_ea_ore'

    @patch('boto3.client')
    def test_sfadmin_db_name_ops_default(self,
                                         client,
                                         ops_minimum_environment_variables,
                                         monkeypatch):
        self.set_environment_vars(ops_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.sfadmin_db_name == 'sfadmin_ops_ore'

    @patch('boto3.client')
    def test_elb_url(self,
                     client,
                     custom_environment_variables,
                     monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.elb_url == 'test_elb_url'

    @patch('boto3.client')
    def test_elb_url_ea_default(self,
                                client,
                                ea_minimum_environment_variables,
                                monkeypatch):
        self.set_environment_vars(ea_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.elb_url == 'lb-ea-ore.starfishsolutions.com'

    @patch('boto3.client')
    def test_elb_url_ops_default(self,
                                 client,
                                 ops_minimum_environment_variables,
                                 monkeypatch):
        self.set_environment_vars(ops_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.elb_url == 'lb-ops-ore.starfishsolutions.com'

    @patch('boto3.client')
    def test_rds_id(self,
                    client,
                    custom_environment_variables,
                    monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.rds_id == 'test_rds_id'

    @patch('boto3.client')
    def test_rds_id_ea_default(self,
                               client,
                               ea_minimum_environment_variables,
                               monkeypatch):
        self.set_environment_vars(ea_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.rds_id == 'sf-rds-ea-single-tenant-dbs02-ore'

    @patch('boto3.client')
    def test_rds_id_ops_default(self,
                                client,
                                ops_minimum_environment_variables,
                                monkeypatch):
        self.set_environment_vars(ops_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.rds_id == 'sf-rds-ops-single-tenant-dbs03-ore'

    @patch('boto3.client')
    def test_rds_replica_id(self,
                            client,
                            custom_environment_variables,
                            monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.rds_replica_id == 'test_rds_replica_id'

    @patch('boto3.client')
    def test_rds_replica_id_ea_default(self,
                                       client,
                                       ea_minimum_environment_variables,
                                       monkeypatch):
        self.set_environment_vars(ea_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.rds_replica_id == 'sf-rds-ea-single-tenant-dbs02-ore'

    @patch('boto3.client')
    def test_rds_replica_id_ops_default(self,
                                        client,
                                        ops_minimum_environment_variables,
                                        monkeypatch):
        self.set_environment_vars(ops_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.rds_replica_id == 'sf-rds-ops-single-tenant-dbs03-ore'

    @patch('boto3.client')
    def test_service_api_success_network_endpoint(self,
                                                  client,
                                                  custom_environment_variables,
                                                  monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.service_api_success_network_endpoint == 'test_ssn_endpoint'

    @patch('boto3.client')
    def test_service_api_success_network_endpoint_ea_default(self,
                                                             client,
                                                             ea_minimum_environment_variables,
                                                             monkeypatch):
        self.set_environment_vars(ea_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.service_api_success_network_endpoint == 'https://blaise-api.hesos.net/sf-success-network-ea/tenants/{tenant_id}/users/{user_id}/'

    @patch('boto3.client')
    def test_service_api_success_network_endpoint_ops_default(self,
                                                              client,
                                                              ops_minimum_environment_variables,
                                                              monkeypatch):
        self.set_environment_vars(ops_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.service_api_success_network_endpoint == 'https://blaise-api.hesos.net/sf-success-network-ops/tenants/{tenant_id}/users/{user_id}/'

    @patch('boto3.client')
    def test_service_api_success_network_key(self,
                                             client,
                                             custom_environment_variables,
                                             monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.service_api_success_network_key == 'test_ssn_key'

    @patch('boto3.client')
    def test_service_api_success_network_key_ea_default(self,
                                                        client,
                                                        ea_minimum_environment_variables,
                                                        monkeypatch):
        self.set_environment_vars(ea_minimum_environment_variables, monkeypatch)
        monkeypatch.setenv('SERVICE_API_SSN_EA_ORE', 'test_ssn_key_ea')
        env = SFTenantEnvironment()
        assert env.service_api_success_network_key == 'test_ssn_key_ea'

    @patch('boto3.client')
    def test_service_api_success_network_key_ops_default(self,
                                                         client,
                                                         ops_minimum_environment_variables,
                                                         monkeypatch):
        self.set_environment_vars(ops_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        monkeypatch.setenv('SERVICE_API_SSN_OPS_ORE', 'test_ssn_key_ops')

        assert env.service_api_success_network_key == 'test_ssn_key_ops'

    @patch('boto3.client')
    def test_service_api_appointments_endpoint(self,
                                               client,
                                               custom_environment_variables,
                                               monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.service_api_appointments_endpoint == 'test_appts_endpoint'

    @patch('boto3.client')
    def test_service_api_appointments_endpoint_ea_default(self,
                                                          client,
                                                          ea_minimum_environment_variables,
                                                          monkeypatch):
        self.set_environment_vars(ea_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.service_api_appointments_endpoint == 'https://blaise-api.hesos.net/sf-appts-ea/tenants/{tenant_id}/users/{user_id}/'

    @patch('boto3.client')
    def test_service_api_appointments_endpoint_ops_default(self,
                                                              client,
                                                              ops_minimum_environment_variables,
                                                              monkeypatch):
        self.set_environment_vars(ops_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.service_api_appointments_endpoint == 'https://blaise-api.hesos.net/sf-appts-ops/tenants/{tenant_id}/users/{user_id}/'

    @patch('boto3.client')
    def test_service_api_appointments_key(self,
                                          client,
                                          custom_environment_variables,
                                          monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.service_api_appointments_key == 'test_appts_key'

    @patch('boto3.client')
    def test_service_api_appointments_key_ea_default(self,
                                                     client,
                                                     ea_minimum_environment_variables,
                                                     monkeypatch):
        self.set_environment_vars(ea_minimum_environment_variables, monkeypatch)
        monkeypatch.setenv('SERVICE_API_APPTS_EA_ORE', 'test_appts_key_ea')
        env = SFTenantEnvironment()
        assert env.service_api_appointments_key == 'test_appts_key_ea'

    @patch('boto3.client')
    def test_service_api_appointments_key_ops_default(self,
                                                      client,
                                                      ops_minimum_environment_variables,
                                                      monkeypatch):
        self.set_environment_vars(ops_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        monkeypatch.setenv('SERVICE_API_APPTS_OPS_ORE', 'test_appts_key_ops')

        assert env.service_api_appointments_key == 'test_appts_key_ops'
        
    @patch('boto3.client')
    def test_service_api_saved_filters_endpoint(self, 
                                                client,
                                                custom_environment_variables,
                                                monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.service_api_saved_filters_endpoint == 'test_ssf_endpoint'

    @patch('boto3.client')
    def test_service_api_saved_filters_endpoint_ea_default(self,
                                                          client,
                                                          ea_minimum_environment_variables,
                                                          monkeypatch):
        self.set_environment_vars(ea_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.service_api_saved_filters_endpoint == 'https://blaise-api.hesos.net/sf-saved-filters-ea-ore/tenants/{tenant_id}/users/{user_id}/'

    @patch('boto3.client')
    def test_service_api_saved_filters_endpoint_ops_default(self,
                                                           client,
                                                           ops_minimum_environment_variables,
                                                           monkeypatch):
        self.set_environment_vars(ops_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.service_api_saved_filters_endpoint == 'https://blaise-api.hesos.net/sf-saved-filters-ops-ore/tenants/{tenant_id}/users/{user_id}/'

    @patch('boto3.client')
    def test_service_api_saved_filters_key(self,
                                          client,
                                          custom_environment_variables,
                                          monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.service_api_saved_filters_key == 'test_ssf_key'

    @patch('boto3.client')
    def test_service_api_saved_filters_key_ea_default(self,
                                                     client,
                                                     ea_minimum_environment_variables,
                                                     monkeypatch):
        self.set_environment_vars(ea_minimum_environment_variables, monkeypatch)
        monkeypatch.setenv('SERVICE_API_SSF_EA_ORE', 'test_saved_filters_key_ea')
        env = SFTenantEnvironment()
        assert env.service_api_saved_filters_key == 'test_saved_filters_key_ea'

    @patch('boto3.client')
    def test_service_api_saved_filters_key_ops_default(self,
                                                      client,
                                                      ops_minimum_environment_variables,
                                                      monkeypatch):
        self.set_environment_vars(ops_minimum_environment_variables, monkeypatch)
        monkeypatch.setenv('SERVICE_API_SSF_OPS_ORE', 'test_saved_filters_key_ops')
        env = SFTenantEnvironment()

        assert env.service_api_saved_filters_key == 'test_saved_filters_key_ops'

    @patch('boto3.client')
    def test_mobile_surveys_enabled(self,
                                    client,
                                    custom_environment_variables,
                                    monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.mobile_surveys_enabled == 'test_mobile_surveys_enabled'

    @patch('boto3.client')
    def test_mobile_surveys_enabled_ea_default(self,
                                               client,
                                               ea_minimum_environment_variables,
                                               monkeypatch):
        self.set_environment_vars(ea_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.mobile_surveys_enabled == 'true'

    @patch('boto3.client')
    def test_mobile_surveys_enabled_ops_default(self,
                                                client,
                                                ops_minimum_environment_variables,
                                                monkeypatch):
        self.set_environment_vars(ops_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.mobile_surveys_enabled == 'false'

    @patch('boto3.client')
    def test_responsive_kiosk_enabled(self,
                                      client,
                                      custom_environment_variables,
                                      monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.responsive_kiosk_enabled == 'test_responsive_kiosk_enabled'

    @patch('boto3.client')
    def test_responsive_kiosk_enabled_ea_default(self,
                                                 client,
                                                 ea_minimum_environment_variables,
                                                 monkeypatch):
        self.set_environment_vars(ea_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.responsive_kiosk_enabled == 'true'

    @patch('boto3.client')
    def test_responsive_kiosk_enabled_ops_default(self,
                                                  client,
                                                  ops_minimum_environment_variables,
                                                  monkeypatch):
        self.set_environment_vars(ops_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.responsive_kiosk_enabled == 'false'

    @patch('boto3.client')
    def test_note(self,
                  client,
                  custom_environment_variables,
                  monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.note == 'test note'
        
    @patch('boto3.client')
    def test_note_ea_default(self,
                             client,
                             ea_minimum_environment_variables,
                             monkeypatch):
        self.set_environment_vars(ea_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.note == ''

    @patch('boto3.client')
    def test_note_ops_default(self,
                              client,
                              ops_minimum_environment_variables,
                              monkeypatch):
        self.set_environment_vars(ops_minimum_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.note == ''    

    @patch('boto3.client')
    def test_workmail_username(self,
                           client,
                           custom_environment_variables,
                           monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.workmail_username == 'test_workmail_username'
        
    @patch('boto3.client')
    def test_workmail_display_name(self,
                                   client,
                                   custom_environment_variables,
                                   monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.workmail_display_name == 'test_workmail_display_name'
        
    @patch('boto3.client')
    def test_workmail_password(self,
                               client,
                               custom_environment_variables,
                               monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.workmail_password == 'test_workmail_password' 
        
    @patch('boto3.client')
    def test_workmail_organization_id(self,
                                           client,
                                           custom_environment_variables,
                                           monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.workmail_organization_id == 'test_organization_id'
        
    @patch('boto3.client')
    def test_host_zone_id(self,
                          client,
                          custom_environment_variables,
                          monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.host_zone_id == 'test_host_zone_id'    
        
    @patch('boto3.client')
    def test_starfish_db_script_dir(self,
                                    client,
                                    custom_environment_variables,
                                    monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        env = SFTenantEnvironment()
        assert env.starfish_db_script_dir == 'tests/sql/starfish-all/web/def/scripts/refresh/'

    @patch('boto3.client')
    def test_rds_endpoint_address(self,
                                  client):
        SFTenantEnvironment.rds_endpoint_address('test_rds_id')
        client().describe_db_instances.assert_called_with(DBInstanceIdentifier='test_rds_id')
