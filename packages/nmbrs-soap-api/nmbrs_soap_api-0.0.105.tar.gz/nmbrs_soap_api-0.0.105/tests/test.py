from src.nmbrs.api import NmbrsSoapAPI

# from nmbrs.api import NmbrsSoapAPI

soap_api = NmbrsSoapAPI({"Username": "lk@incomme.nl", "Token": "739daa8a334d4918a9ffef0d0ba984b5"})

print(soap_api.auth_header)

