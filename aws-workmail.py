#!/usr/bin/python
import boto3
import os
import sys
import logging
from botocore.exceptions import ClientError

"""Class for AWS Workmail creations"""
class AWSMailbox:
    def __init__(self,loglevel):
        logging.basicConfig(level=loglevel)
        self.rootLogger = logging.getLogger()
    
    def set_organization_subdomain(self,organization_id,subdomain):
        """Function to set organization_id and Subdomain."""
        self.organization_id = organization_id
        self.subdomain = subdomain
    
    def set_aws_profile(self,region,access_key,secret_key):
        """Function to set AWS profile & Region."""
        self.aws_access_key_id = access_key
        self.aws_secret_access_key = secret_key
        self.aws_region = region
        self.rootLogger.info("key, secretkey and region set successfully")
    
    def set_mailbox_profile(self,userid,displayname,password):
        """Function to set Mail Box Profile."""
        self.user_id = userid
        self.display_name = displayname
        self.email_password = password
        self.rootLogger.info("userid, displayname, password set successfully")
    
    def cloud_connect(self):
        """Function to Connect to AWS."""
        self.rootLogger.info("creating workmail client to workmail using access_key and secretkey")
        try:
            self.boto3_client = boto3.client('workmail',
                                             aws_access_key_id = self.aws_access_key_id,
                                             aws_secret_access_key = self.aws_secret_access_key,
                                             region_name = self.aws_region,
                                             )
        except ClientError as cerr:
            self.rootLogger.critical("Connection error: %s" % cerr)
            sys.exit(0)
        
        if(self.boto3_client):
            self.rootLogger.info("Workmail client created successfully")
        else:
            self.rootLogger.critical("Connection Error!. Please check AWS Settings")
            sys.exit(0)

    def create_mailbox(self):
        """Function to create Mail Box."""
        self.rootLogger.info("Trying to authenticate and create workmail mailbox")
        user_id_created=None
        try:
            response = self.boto3_client.create_user(
                                                    OrganizationId = self.organization_id,
                                                    Name = self.user_id,
                                                    DisplayName = self.display_name,
                                                    Password = self.email_password
                                                    )
                
            user_id_created=response['UserId']
            self.rootLogger.info("Created account with user id: " + user_id_created)
        except ClientError as e:
            self.rootLogger.critical("Unexpected error while creating user: %s" % e)

        # Mail box creation is success, activate it.
        if(user_id_created is not None):
            self.rootLogger.info("Registering the user id : " + user_id_created)
            self.rootLogger.info("Register: OrganizationId set as: " + self.organization_id)
            self.rootLogger.info("Register: EntityId set as: " + user_id_created)
            self.rootLogger.info("Register: Email set as: " + self.user_id+"@" + self.subdomain)
            try:
                response1 = self.boto3_client.register_to_work_mail(
                                                                    
                                                                    OrganizationId=self.organization_id,
                                                                    EntityId=user_id_created,
                                                                    Email=self.user_id+"@" + self.subdomain
                                                                    )
                self.rootLogger.info("Successfully registered in the domain user id : " + user_id_created)
            except ClientError as e:
                self.rootLogger.critical("Unexpected error: %s" % e)
            self.rootLogger.info("Registered mailbox successfully. User-id: " + user_id_created )

"""CLASS Defeniton End here"""
"""Main here"""
if __name__ == "__main__":
    loglevel=0
    if(os.getenv('LOG_LEVEL') is None):
        loglevel="0"
    else:
        loglevel=os.getenv('LOG_LEVEL')
    
    if (loglevel in ["50","40","30","20","10","0"]):
        print ("")
    else:
        print ("Invalid LOG_LEVEL value found. Supported values are : (50,40,30,20,10,0)")
        sys.exit(1)
    
    aws_workmail=AWSMailbox(int(loglevel))
    
    aws_workmail.set_aws_profile("us-east-1",os.getenv('AWS_KEY'),os.getenv('AWS_SECRET'))
    aws_workmail.cloud_connect()
    aws_workmail.set_organization_subdomain("<YOUR organization ID>","<your Subdomin>")
    aws_workmail.set_mailbox_profile("user108","My Display Name", "MyPassword@123")
    aws_workmail.create_mailbox()
