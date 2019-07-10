import psycopg2
import re

from typing import List
from sfenv import SFTenantEnvironment

class TenantDBCreator:
    """Creates new tenant dbs"""
    _create_db_script_path = 'sql/create_tenant_db.sql'
    _sfadmin_script_path = 'sql/add_admin_data_source.sql'

    def __init__(self, env: SFTenantEnvironment) -> None:
        self.env = env

        with open('sql/tenant_db_init_scripts.txt', 'r') as script_list:
            script_names = script_list.read().splitlines()

        self._new_db_script_paths = [
            'sql/set_up.sql'
        ] + [self.env.starfish_db_script_dir + name for name in script_names]

    @property
    def tenant_db_create_script(self) -> str:
        """Return create db script from stored path"""
        return self.read_sql_script(self._create_db_script_path)

    @property
    def sfadmin_script(self) -> str:
        """Return sfadmin script from stored path"""
        return self.read_sql_script(self._sfadmin_script_path)

    @property
    def new_db_scripts(self) -> List[str]:
        """Return list of scripts from stored path"""
        new_db_scripts = []
        for path in self._new_db_script_paths:
            new_db_scripts.append(self.read_sql_script(path))
        return new_db_scripts

    def read_sql_script(self, file_path: str) -> str:
        """Return sql from given path with placeholders replaced"""
        with open(file_path) as file:
            return self.replace_placeholders(file.read())

    def replace_placeholders(self, file_content: str) -> str:
        """Replace Jenkins placeholders with matching environment variables"""
        altered_file_content = file_content
        for placeholder in re.findall('JENKINS_PLACEHOLDER_[A-Z_]+', file_content):
            altered_file_content = re.sub(placeholder,
                                          getattr(self.env, re.findall('(?<=JENKINS_PLACEHOLDER_)[A-Z_]+', placeholder)[0].lower()),
                                          altered_file_content)
        return altered_file_content

    def execute_queries(self,
                        queries: List[str],
                        db_host: str = '',
                        db_name: str = '') -> None:
        """Opens and closes a database connection to execute queries"""
        with psycopg2.connect(host=db_host,
                              user=self.env.postgres_user,
                              password=self.env.postgres_password,
                              database=db_name) as conn:
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            for query in queries:
                with conn.cursor() as cursor:
                    cursor.execute(query)

    def create_tenant_db(self) -> None:
        self.execute_queries([self.tenant_db_create_script],
                             db_host=self.env.db_hostname,
                             db_name=self.env.base_db_name)

    def set_up_tenant_db(self) -> None:
        self.execute_queries(self.new_db_scripts,
                             db_host=self.env.db_hostname,
                             db_name=self.env.db_name)

    def update_sfadmin_db(self) -> None:
        self.execute_queries([self.sfadmin_script],
                             db_host=self.env.sfadmin_db_hostname,
                             db_name=self.env.sfadmin_db_name)
