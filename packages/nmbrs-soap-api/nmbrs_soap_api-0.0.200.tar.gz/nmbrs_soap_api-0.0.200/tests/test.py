from nmbrs import NmbrsSoapAPI


api = NmbrsSoapAPI(username="lk@incomme.nl", token="739daa8a334d4918a9ffef0d0ba984b5")
companies = api.company_service.get_all()

company_map = []

for company in companies:
    wage_tax = api.company_service.get_all_wagetax(company.id, 2024)

    if len(wage_tax) > 0:
        xml = api.company_service.get_wagetax_details(company.id, wage_tax[0].loonaangifte_id)
        xml = xml.to_dict()
        company_map.append({"id": company.id, "wage_tax": xml["xml"]["Loonaangifte"]["AdministratieveEenheid"]["LhNr"]})
