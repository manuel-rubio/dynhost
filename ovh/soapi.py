from SOAPpy import WSDL
from dymmer.settings import WSDL_FILE, OVH_USER, OVH_PASS, DOMAIN_CONTACT, DNS_CONFIG, DEBUG, OVH_USERS_PASS

soap = WSDL.Proxy(WSDL_FILE)

def login(username=OVH_USER, password=OVH_PASS):
    return soap.login(username, password, 'en', 0)

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

# country: es|fr|be|pt|ch|de|...
# language: fr|en|es|...
# legalform: corporation|individual|association|other
def nic_create(name, firstname, password, email, phone, fax, address, 
               city, area, zipCode, country, language, legalform,
               organisation, legalName, legalNumber, vat):
    session = login()
    isOwner = 0
    result = soap.nicCreate(
        session, name, firstname, password,
        email, phone, fax, address, city, area,
        zipCode, country, language, isOwner, legalform,
        organisation, legalName, legalNumber, vat)
    soap.logout(session)
    return result

def renew_domain(domain):
    session = login()
    dryRun = 1 if DEBUG else 0
    result = soap.resellerDomainRenew(
        session, domain, dryRun)
    soap.logout(session)
    return result

def buy_domain(domain, nic):
    session = login()
    hosting = 'none'
    offer = 'gold'
    owo = 'no'
    reseller_profile = 'whiteLabel' # none, whiteLabel, agent
    owner = nic
    admin = DOMAIN_CONTACT
    tech = DOMAIN_CONTACT
    billing = DOMAIN_CONTACT
    dns1, dns2, dns3, dns4 = DNS_CONFIG
    method = ''       # only for .fr
    legalName = ''    # only for .fr
    legalNumber = ''  # only for .fr
    afnicldent = ''   # only for .fr
    birthDate = ''    # only for .fr
    birthCity = ''    # only for .fr
    birthDepart = ''  # only for .fr
    birthCountry = '' # only for .fr
    dryRun = 1 if DEBUG else 0
    result = soap.resellerDomainCreate(
        session, domain, hosting, offer,
        reseller_profile, owo,
        owner, admin, tech, billing,
        dns1, dns2, dns3, dns4, '',
        method, legalName, legalNumber,
        afnicldent, birthDate, birthCity,
        birthDepart, birthCountry, dryRun)
    soap.logout(session)
    return result

def transfer_domain(domain, nic, authinfo):
    session = login()
    hosting = 'none'
    offer = 'gold'
    owo = 'no'
    reseller_profile = 'whiteLabel' # none, whiteLabel, agent
    owner = nic
    admin = DOMAIN_CONTACT
    tech = DOMAIN_CONTACT
    billing = DOMAIN_CONTACT
    dns1, dns2, dns3, dns4 = DNS_CONFIG
    method = ''       # only for .fr
    legalName = ''    # only for .fr
    legalNumber = ''  # only for .fr
    afnicldent = ''   # only for .fr
    birthDate = ''    # only for .fr
    birthCity = ''    # only for .fr
    birthDepart = ''  # only for .fr
    birthCountry = '' # only for .fr
    dryRun = 1 if DEBUG else 0
    result = soap.resellerDomainTransfer(
        session, domain, authinfo, hosting, offer,
        reseller_profile, owo, owner, admin, tech,
        billing, dns1, dns2, dns3, dns4, '',
        method, legalName, legalNumber, afnicldent,
        birthDate, birthCity, birthDepart, 
        birthCountry, dryRun)
    soap.logout(session)
    return result
