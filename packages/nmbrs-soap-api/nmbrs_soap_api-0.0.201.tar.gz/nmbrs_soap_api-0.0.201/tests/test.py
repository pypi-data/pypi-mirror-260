from nmbrs import NmbrsSoapAPI


api = NmbrsSoapAPI(username="lars.kluijtmans@gmail.com", token="505deed6df9f42879e91a58bcad53812")
debtors = api.debtor_service.get_all()
created = api.debtor_service.insert(2522001, "2522001", "lars kluijtmans")
print(created)
debtor = api.debtor_service.get(2522001)
print(debtor)
api.debtor_service.update(2522001, "--2522001", "lars kluijt")
debtor = api.debtor_service.get(2522001)
print(debtor)
