from nmbrs.api import NmbrsSoapAPI

api = NmbrsSoapAPI({"Username": "lk@incomme.nl", "Token": "739daa8a334d4918a9ffef0d0ba984b5"})

debtors = api.debtor_service.get_all()

print(len(debtors))