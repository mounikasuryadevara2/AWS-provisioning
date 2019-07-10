import pytest

from unittest.mock import MagicMock, patch

from sfenv import SFTenantEnvironment
from sfmail import TenantWorkmailCreator


class TestTenantWorkmailCreator:
    def set_environment_vars(self, vars: dict, monkeypatch):
        for key in vars:
            monkeypatch.setenv(key, vars[key])

    @patch('boto3.client')
    def test_create_mailbox_user(self, client, ea_minimum_environment_variables, monkeypatch):
        self.set_environment_vars(ea_minimum_environment_variables, monkeypatch)
        
        TenantWorkmailCreator(SFTenantEnvironment()).create_mailbox_user()

        client().create_user.assert_called_with(OrganizationId='test_organization_id',
                                              Name='test_workmail_username',
                                              DisplayName='test_workmail_display_name',
                                              Password='test_workmail_password')

    @patch('boto3.client')
    def test_create_mailbox(self, client, ea_minimum_environment_variables, monkeypatch):
        self.set_environment_vars(ea_minimum_environment_variables, monkeypatch)
        
        TenantWorkmailCreator(SFTenantEnvironment(), mailbox_user_id='test_id').create_mailbox()

        client().register_to_work_mail.assert_called_with(OrganizationId='test_organization_id',
                                                        EntityId='test_id',
                                                        Email='test_workmail_username' + '@' + 'test')
