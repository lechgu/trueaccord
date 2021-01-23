import iso8601


# entities to be consumed
class Debt:
    def __init__(self, *, amount, id, **kwargs):
        self.amount = amount
        self.id = id
        self.payment_plan = None
        # ignore everything else


class PaymentPlan:
    def __init__(
        self,
        amount_to_pay,
        debt_id,
        id,
        installment_amount,
        installment_frequency,
        start_date,
        **kwargs
    ):
        self.amount_to_pay = amount_to_pay
        self.debt_id = debt_id
        self.id = id
        self.installment_amount = installment_amount
        self.installment_frequency = installment_frequency
        self.start_date = iso8601.parse_date(start_date)
        self.payments = []
        # ignore everything else


class Payment:
    def __init__(self, amount, date, payment_plan_id, **kwargs):
        self.amount = amount
        self.date = iso8601.parse_date(date)
        self.payment_plan_id = payment_plan_id
        # ignore everything else


# entity to be emitted
class DebtInfo:
    def __init__(self, debt, next_date):
        self.id = debt.id
        self.amount = debt.amount
        self.is_in_payment_plan = debt.payment_plan is not None
        if next_date:
            self.next_payment_due_date = next_date
        else:
            self.next_payment_due_date = None
