import json

import requests

from debts import date_serializer
from debts.db import Database
from debts.entities import Debt, Payment, PaymentPlan

# hardcode urls, for now
debts_url = (
    "https://my-json-server.typicode.com/druska/"
    "trueaccord-mock-payments-api/debts"
)
pplans_url = (
    "https://my-json-server.typicode.com/druska/"
    "trueaccord-mock-payments-api/payment_plans"
)
payments_url = (
    "https://my-json-server.typicode.com/druska/"
    "trueaccord-mock-payments-api/payments"
)

if __name__ == "__main__":
    # pull stuff from the endpoints
    r = requests.get(debts_url)
    payload = r.json()
    debts = [Debt(**item) for item in r.json()]
    r = requests.get(pplans_url)
    payload = r.json()
    payment_plans = [PaymentPlan(**item) for item in payload]
    r = requests.get(payments_url)
    payload = r.json()
    payments = [Payment(**item) for item in payload]
    # initialize the database
    db = Database(debts, payment_plans, payments)
    # dump all database info, as requested,
    # each line is json-formatted debt info
    for debt_info in db.enumerate_debt_infos():
        print(json.dumps(debt_info.__dict__, default=date_serializer))
