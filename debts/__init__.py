import datetime

# misc stuff

NEXT_PAYMENT_CALCULATORS = {
    "BI_WEEKLY": lambda last_date: last_date + datetime.timedelta(weeks=2),
    "WEEKLY": lambda last_date: last_date + datetime.timedelta(weeks=1),
}


def date_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return obj.date().isoformat()
    raise TypeError("Unknown type")
