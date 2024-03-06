from nmbrs import api
from nmbrs import NmbrsSoapAPI


api.standard_auth("lk@incomme.nl", "739daa8a334d4918a9ffef0d0ba984b5")
debtors = api.debtor_service.get_all()
print(len(debtors))

api = NmbrsSoapAPI(username="lk@incomme.nl", token="739daa8a334d4918a9ffef0d0ba984b5")
debtors = api.debtor_service.get_all()
print(len(debtors))
