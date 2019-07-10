import pytest

from unittest.mock import patch, MagicMock

from sfdns import TenantDNSCreator
from sfenv import SFTenantEnvironment

class TestTenantDNSCreator(object):
    def set_environment_vars(self, vars: dict, monkeypatch):
        for key in vars:
            monkeypatch.setenv(key, vars[key])

    @patch('boto3.client')
    def test_set_ELB_dns(self,
                         client,
                         custom_environment_variables,
                         monkeypatch):
        self.set_environment_vars(custom_environment_variables,
                                  monkeypatch)
        TenantDNSCreator(SFTenantEnvironment()).set_ELB_dns()
        client().change_resource_record_sets.assert_called_with(HostedZoneId='test_host_zone_id',
                                                                ChangeBatch={
                'Comment': 'sfdns.py',
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {

                        'ResourceRecords': [
                        {
                            'Value': 'test'
                        }
                        ],
                        'Name': 'test_elb_url',
                        'Type': 'CNAME',
                        'TTL': 300
                        }
                    },
                ]
            })
            

    @patch('boto3.client')
    def test_set_DB_dns(self,
                        client,
                        custom_environment_variables,
                        monkeypatch):
        self.set_environment_vars(custom_environment_variables,
                                  monkeypatch)
        env = SFTenantEnvironment()
        TenantDNSCreator(env).set_DB_dns()
        
        client().change_resource_record_sets.assert_called_with(HostedZoneId='test_host_zone_id',
                                                                ChangeBatch={
                'Comment': 'sfdns.py',
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {

                            'ResourceRecords': [
                                {
                                    'Value': 'test_rds_id'
                                }
                            ],
                            'Name': env.db_hostname,
                            'Type': 'CNAME',
                            'TTL': 300
                        }
                    },
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {

                            'ResourceRecords': [
                                {
                                    'Value': 'test_rds_replica_id'
                                }
                            ],
                            'Name': env.replica_db_hostname,
                            'Type': 'CNAME',
                            'TTL': 300
                        }
                    },
                ]
            })
            
