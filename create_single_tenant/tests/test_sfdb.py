import pytest

from unittest.mock import patch, PropertyMock, MagicMock

from sfdb import TenantDBCreator
from sfenv import SFTenantEnvironment


class TestTenantDBCreator:
    def set_environment_vars(self, vars: dict, monkeypatch):
        for key in vars:
            monkeypatch.setenv(key, vars[key])

    @patch('boto3.client')
    def test_tenant_db_creator(self,
                               client,
                               custom_environment_variables,
                               monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        db_creator = TenantDBCreator(SFTenantEnvironment())
        assert db_creator._create_db_script_path == 'sql/create_tenant_db.sql'
        assert db_creator._sfadmin_script_path == 'sql/add_admin_data_source.sql'
        assert db_creator._new_db_script_paths == [
            'sql/set_up.sql',
            'tests/sql/starfish-all/web/def/scripts/refresh/createOnly.sql',
            'tests/sql/starfish-all/web/def/scripts/refresh/dataOnly_prod.sql',
            'tests/sql/starfish-all/web/def/scripts/refresh/messageTemplateData.sql',
            'tests/sql/starfish-all/web/def/scripts/refresh/functionOnly.sql',
            'tests/sql/starfish-all/web/def/scripts/refresh/triggerOnly.sql',
            'tests/sql/starfish-all/web/def/scripts/refresh/createFlagExperiments.sql',
            'tests/sql/starfish-all/web/def/scripts/refresh/updateFlagExperiments.sql'
        ]

    @patch('boto3.client')
    def test_read_sql_script(self,
                             client,
                             custom_environment_variables,
                             monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        db_creator = TenantDBCreator(SFTenantEnvironment())
        assert db_creator.read_sql_script('sql/create_tenant_db.sql') == 'create database test_db;\n'

    @patch('boto3.client')
    def test_tenant_db_create_script(self,
                              client,
                              custom_environment_variables,
                              monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        db_creator = TenantDBCreator(SFTenantEnvironment())
        assert db_creator.tenant_db_create_script == 'create database test_db;\n'

    @patch('boto3.client')
    def test_sfadmin_script(self,
                            client,
                            custom_environment_variables,
                            monkeypatch):
        client().describe_db_instances().DBInstances.__getitem__().Endpoint.Address.return_value = 'test_address'
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        db_creator = TenantDBCreator(SFTenantEnvironment())
        assert db_creator.sfadmin_script == (
            "INSERT INTO data_source (data_source_id,\n"
            "                         db_url,\n"
            "                         calendar_email,\n"
            "                         calendar_host,\n"
            "                         support_email,\n"
            "                         support_host,\n"
            "                         db_url_read_replica)\n"
            "VALUES (upper('test_db'),\n"
            "        'jdbc:postgresql://test_address/test_db',\n"
            "        'test@calendar.starfishsolutions.com',\n"
            "        'imap.mail.us-west-2.awsapps.com',\n"
            "        'Not Used',\n"
            "        'Not Used',\n"
            "        'jdbc:postgresql://test_address/test_db');\n"
        )

    @patch('boto3.client')
    def test_new_db_scripts(self,
                            client,
                            custom_environment_variables,
                            monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        db_creator = TenantDBCreator(SFTenantEnvironment())
        assert db_creator.new_db_scripts == [
            ('alter group starfish add user batch, importer, admin;\n'
             'alter user starfish set temp_buffers = \'32MB\';\n'
             'alter user importer set temp_buffers = \'32MB\';\n'
             'alter user admin set temp_buffers = \'32MB\';\n'
             'alter user devuser set temp_buffers = \'32MB\';\n'
             'alter user batch set temp_buffers = \'256MB\';\n'
             'create extension "uuid-ossp";\n'
             'create extension hstore;\n'
             'create extension pg_stat_statements;\n'
             'create extension if not exists pg_repack;\n'
             'insert into sf_metadata (metadata_name, metadate_val) values (\'patch\', \'testbranch.0\');\n'
             'insert into sf_metadata (metadata_name, metadate_val) values (\'functions\', \'testbranch.0\');\n'
             'insert into sf_metadata (metadata_name, metadate_val) values (\'triggers\', \'testbranch.0\');\n'
             'insert into sf_metadata (metadata_name, metadate_val) values (\'flagExperiments\', \'testbranch.0\');\n'
            ),
            'testsql1\n',
            'testsql2\n',
            'testsql3\n',
            'testsql4\n',
            'testsql5\n',
            'testsql6\n',
            'testsql7\n'
        ]

    @patch('boto3.client')
    def test_replace_placeholders(self,
                                  client,
                                  custom_environment_variables,
                                  monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        db_creator = TenantDBCreator(SFTenantEnvironment())
        assert db_creator.replace_placeholders(
            'JENKINS_PLACEHOLDER_SUBDOMAIN./do_not_replace_ /.JENKINS_PLACEHOLDER_DB_NAME'
        ) == 'test./do_not_replace_ /.test_db'

    @patch('psycopg2.connect')
    @patch('boto3.client')
    def test_execute_queries(self,
                             client,
                             connect,
                             custom_environment_variables,
                             monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        db_creator = TenantDBCreator(SFTenantEnvironment())

        db_creator.execute_queries(['select * from test;',
                                         'select * from test2;'],
                                        db_host='test_host',
                                        db_name='test_db')
        connect.assert_called_with(database='test_db',
                                   host='test_host',
                                   user='test_pg_user',
                                   password='test_pg_password')
        connect().__enter__().set_isolation_level.assert_called_with(0)
        connect().__enter__().cursor().__enter__().execute.assert_any_call(
            'select * from test;'
        )
        connect().__enter__().cursor().__enter__().execute.assert_any_call(
            'select * from test2;'
        )

    @patch.object(TenantDBCreator, 'execute_queries')
    @patch.object(TenantDBCreator, 'tenant_db_create_script', new_callable=PropertyMock)
    @patch('boto3.client')
    def test_create_tenant_db(self,
                              client,
                              mock_tenant_db_create_script,
                              mock_execute_queries,
                              custom_environment_variables,
                              monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        db_creator = TenantDBCreator(SFTenantEnvironment())
        db_creator.create_tenant_db()
        mock_tenant_db_create_script.assert_called_once()
        mock_execute_queries.assert_called_once()

    @patch.object(TenantDBCreator, 'execute_queries')
    @patch.object(TenantDBCreator, 'new_db_scripts', new_callable=PropertyMock)
    @patch('boto3.client')
    def test_set_up_tenant_db(self,
                              client,
                              mock_new_db_scripts,
                              mock_execute_queries,
                              custom_environment_variables,
                              monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        db_creator = TenantDBCreator(SFTenantEnvironment())
        db_creator.set_up_tenant_db()
        mock_new_db_scripts.assert_called_once()
        mock_execute_queries.assert_called_once()

    @patch.object(TenantDBCreator, 'execute_queries')
    @patch.object(TenantDBCreator, 'sfadmin_script', new_callable=PropertyMock)
    @patch('boto3.client')
    def test_update_sfadmin_db(self,
                              client,
                              mock_sfadmin_script,
                              mock_execute_queries,
                              custom_environment_variables,
                              monkeypatch):
        self.set_environment_vars(custom_environment_variables, monkeypatch)
        db_creator = TenantDBCreator(SFTenantEnvironment())
        db_creator.update_sfadmin_db()
        mock_sfadmin_script.assert_called_once()
        mock_execute_queries.assert_called_once()
