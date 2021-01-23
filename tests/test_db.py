import datetime

from debts.entities import Payment, PaymentPlan, Debt
from debts.db import Database


def test_unassociated_loan():
    today = datetime.datetime.utcnow()

    debt = Debt(amount=100.0, id=1)
    pplan = PaymentPlan(
        id=42,
        debt_id=100,
        installment_amount=1000.0,
        installment_frequency="WEEKLY",
        amount_to_pay=10.0,
        start_date=today.date().isoformat(),
    )

    debts = [debt]
    pplans = [pplan]
    payments = []
    db = Database(debts, pplans, payments)
    infos = list(db.enumerate_debt_infos())
    assert len(infos) == 1
    assert not infos[0].is_in_payment_plan
    assert infos[0].next_payment_due_date is None


def test_paid_loan():
    today = datetime.datetime.utcnow()
    start = today - datetime.timedelta(days=365)

    debt = Debt(amount=1000.0, id=1)
    pplan = PaymentPlan(
        id=42,
        debt_id=1,
        installment_amount=100.0,
        installment_frequency="WEEKLY",
        amount_to_pay=10.0,
        start_date=start.isoformat(),
    )
    cur = start
    payments = []
    for i in range(10):
        payment = Payment(
            amount=100.0, date=cur.isoformat(), payment_plan_id=42
        )
        payments.append(payment)
        cur += datetime.timedelta(weeks=1)

    debts = [debt]
    pplans = [pplan]
    db = Database(debts, pplans, payments)
    infos = list(db.enumerate_debt_infos())
    assert len(infos) == 1
    assert infos[0].next_payment_due_date is None


def test_unpaid_loan():
    today = datetime.datetime.utcnow()
    start = today - datetime.timedelta(days=365)

    debt = Debt(amount=1000.0, id=1)
    pplan = PaymentPlan(
        id=42,
        debt_id=1,
        installment_amount=100.0,
        installment_frequency="WEEKLY",
        amount_to_pay=10.0,
        start_date=start.isoformat(),
    )
    cur = start
    payments = []
    for i in range(9):
        payment = Payment(
            amount=100.0, date=cur.isoformat(), payment_plan_id=42
        )
        payments.append(payment)
        cur += datetime.timedelta(weeks=1)

    debts = [debt]
    pplans = [pplan]
    db = Database(debts, pplans, payments)
    infos = list(db.enumerate_debt_infos())
    assert len(infos) == 1
    assert infos[0].next_payment_due_date is not None
    expected = db.get_next_payment_date(debt).date()
    actual = infos[0].next_payment_due_date.date()
    assert expected == actual
