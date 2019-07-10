from sfenv import SFTenantEnvironment
from sfdb import TenantDBCreator
from sfdns import TenantDNSCreator
from sfmail import TenantWorkmailCreator

env = SFTenantEnvironment()

db_creator = TenantDBCreator(env)
dns_creator = TenantDNSCreator(env)
mailbox_creator = TenantWorkmailCreator(env)

db_creator.create_tenant_db()
db_creator.set_up_tenant_db()
db_creator.update_sfadmin_db()

dns_creator.set_ELB_dns()
dns_creator.set_DB_dns()

mailbox_creator.create_mailbox_user()
mailbox_creator.create_mailbox()
