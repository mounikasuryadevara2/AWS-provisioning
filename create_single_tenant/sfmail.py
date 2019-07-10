import boto3
import os
import sys
import logging

from botocore.exceptions import ClientError
from sfenv import SFTenantEnvironment

class TenantWorkmailCreator:
    """Class for AWS Workmail creation"""
    def __init__(self, env: SFTenantEnvironment, mailbox_user_id: str = '') -> None:
        self.env = env
        self.mailbox_user_id = mailbox_user_id
        self.boto3_client = boto3.client('workmail')

    def create_mailbox_user(self):
        """Function to create Mail Box."""
        logging.info('Creating mailbox user.')
        self.mailbox_user_id = self.boto3_client.create_user(OrganizationId=self.env.workmail_organization_id,
                                                             Name=self.env.workmail_username,
                                                             DisplayName=self.env.workmail_display_name,
                                                             Password=self.env.workmail_password)['UserId']
        
        logging.info("Registering the user id: " + self.mailbox_user_id)
        logging.info("Register: OrganizationId set as: " + self.env.workmail_organization_id)
        logging.info("Register: EntityId set as: " + self.mailbox_user_id)
        logging.info("Register: Email set as: " + self.env.workmail_username + "@" + self.env.subdomain)

    def create_mailbox(self):
        logging.info('Creating mailbox.')  
        self.boto3_client.register_to_work_mail(OrganizationId=self.env.workmail_organization_id,
                                                EntityId=self.mailbox_user_id,
                                                Email=self.env.workmail_username + "@" + self.env.subdomain) 
        
        logging.info("Register: OrganizationId set as: " + self.env.workmail_organization_id)
        logging.info("Register: EntityId set as: " + self.mailbox_user_id)
        logging.info("Register: Email set as: " + self.env.workmail_username + "@" + self.env.subdomain)
        logging.info("Registered mailbox successfully. User-id: " + self.mailbox_user_id)
