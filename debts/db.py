import datetime

from debts import NEXT_PAYMENT_CALCULATORS
from debts.entities import DebtInfo


# in-memory database which wires together all stuff
class Database:
    def __init__(self, debts, pplans, payments):
        # self.debts is a dict of all debts, keyed by id
        self.debts = {debt.id: debt for debt in debts}
        # self.pplans is a dict of all payment plans, keyed by id
        self.pplans = {pp.id: pp for pp in pplans}
        # append payments to their payment_plans
        for payment in payments:
            if payment.payment_plan_id in self.pplans:
                pplan = self.pplans[payment.payment_plan_id]
                pplan.payments.append(payment)
        # wire payment plans to debts
        # at the same time sort all payments for the plan by date
        for pplan in self.pplans.values():
            d_id = pplan.debt_id
            if d_id in self.debts:
                self.debts[d_id].payment_plan = pplan
            pplan.payments.sort(key=lambda p: p.date)

    def get_next_payment_date(self, debt):
        if debt.payment_plan:
            pplan = debt.payment_plan
            if pplan:
                # calculate how much paid:
                paid = sum(payment.amount for payment in pplan.payments)
                if paid < debt.amount:

                    assert (
                        pplan.installment_frequency in NEXT_PAYMENT_CALCULATORS
                    )
                    calculator = NEXT_PAYMENT_CALCULATORS[
                        pplan.installment_frequency
                    ]

                    return calculator(pplan.payments[-1].date)

            return None

    def enumerate_debt_infos(self):
        for debt in self.debts.values():
            yield DebtInfo(debt, self.get_next_payment_date(debt))
