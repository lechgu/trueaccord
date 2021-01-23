import datetime
import json

from debts import date_serializer
from debts.entities import Debt, Payment, PaymentPlan


def test_debt_json_serialize():
    debt = Debt(amount=100, id=42)
    json_str = json.dumps(debt.__dict__)
    deserialized = json.loads(json_str)
    debt2 = Debt(**deserialized)
    assert debt.amount == debt2.amount
    assert debt.id == debt2.id


def test_pplan_json_serialize():
    today = datetime.datetime.utcnow().date()
    pplan = PaymentPlan(
        id=25,
        amount_to_pay=100.0,
        debt_id=42,
        installment_amount=1000.0,
        installment_frequency="WEEKLY",
        start_date=today.isoformat(),
    )
    json_str = json.dumps(pplan.__dict__, default=date_serializer)
    deserialized = json.loads(json_str)
    pplan2 = PaymentPlan(**deserialized)
    assert pplan.id == pplan2.id
    assert pplan.amount_to_pay == pplan2.amount_to_pay
    assert pplan.debt_id == pplan2.debt_id
    assert pplan.installment_amount == pplan2.installment_amount
    assert pplan.installment_frequency == pplan2.installment_frequency
    assert pplan2.start_date == pplan2.start_date


def test_payment_json_serialize():
    today = datetime.datetime.utcnow().date()
    payment = Payment(amount=10.0, date=today.isoformat(), payment_plan_id=25)
    json_str = json.dumps(payment.__dict__, default=date_serializer)
    deserialized = json.loads(json_str)
    payment2 = Payment(**deserialized)
    assert payment.amount == payment2.amount
    assert payment.date == payment2.date
    assert payment.payment_plan_id == payment2.payment_plan_id