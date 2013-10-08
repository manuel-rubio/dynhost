from SOAPpy import WSDL
from dynhost.settings import WSDL_FILE, OVH_USER, OVH_PASS

soap = WSDL.Proxy(WSDL_FILE)

def login():
	return soap.login(OVH_USER, OVH_PASS, 'es', 0)

def check_domain(domain):
	session = login()
	result = soap.domainCheck(session, domain)
	opts = {}
	for i in result['item']:
		predicate = i['predicate']
		value = i['value']
		reason = i['reason']
		opts[predicate] = [value, reason]
	soap.logout(session)
	return opts
