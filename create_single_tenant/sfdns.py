import boto3
import os
import sys
import logging

from botocore.exceptions import ClientError
from sfenv import SFTenantEnvironment

class TenantDNSCreator:
    """Class for AWS Route53 functions """
    def __init__(self, env: SFTenantEnvironment) -> None:
        self.env = env
        self.boto3_client = boto3.client('route53')

    def set_ELB_dns(self):
        """Function to create DNS Entry for ELB."""
        logging.info('Starting ELB DNS entry request.')
        
        self.boto3_client.change_resource_record_sets(
            HostedZoneId = self.env.host_zone_id,
            ChangeBatch={
                'Comment': 'sfdns.py',
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                                
                        'ResourceRecords': [
                        {
                            'Value': self.env.subdomain
                        }
                        ],
                        'Name': self.env.elb_url,
                        'Type': 'CNAME',
                        'TTL': 300
                        }
                    },
                ]
            }
        )
        
    def set_DB_dns(self):
        """Function to create DNS Entry for db replica."""
        logging.info('Starting DB DNS entry request.')
        
        self.boto3_client.change_resource_record_sets(
            HostedZoneId = self.env.host_zone_id,
            ChangeBatch={
                'Comment': 'sfdns.py',
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            
                        'ResourceRecords': [
                        {
                            'Value': self.env.rds_id
                        }
                        ],
                        'Name': self.env.db_hostname,
                        'Type': 'CNAME',
                        'TTL': 300
                        }
                    },
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                                
                        'ResourceRecords': [
                        {
                            'Value': self.env.rds_replica_id
                        }
                        ],
                        'Name': self.env.replica_db_hostname,
                        'Type': 'CNAME',
                        'TTL': 300
                        }
                    },
                ]
            }
        )

