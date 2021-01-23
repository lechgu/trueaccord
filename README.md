#### Assumptions

- the data provided from the web service returns valid and consistent json. No extra validation is performed
- if the loan is unpaid, the next date is calculated by taking the last payment's date and adding the interval indicated by the payment_frequency value.
- BI-WEEKLY means every 2 weeks, not twice a week.

If any of these is not correct, please let me know I will change the code

##### Implementation notes

- we have entities to consume the json which comes from the web service: Debt, Payment, PaymentPlan as well as entities emitted to be printed to stdout (DebtInfo) entities mostly exist to perform json in-and-out serialization. As such, they usually accept json-compatible types, e.g. strings, but store internally data in more efficient format, when appropriate (e.g. datetime)
- the Database class wires everything together, e.g payment plans to debts, and also enumerates the requested DebtInfos
- UTC is used everywhere

#### Programming environment

I use Python 3.9, on the latest. The following extra packages are used:

- `requests`, the most straightforward way to make http calls.
- `pytest`, for unit testing
- `iso8601`, for parsing iso 8601 dates

#### Set up

- Create the virtual environment:

```
python3 -m venv .venv
```

- activate the virtual environment (Mac or Linux):

```
source .venv/bin/activate
```

- on Windows:

```
.venv\scripts\activate
```

- install the dependencies:

```
pip install -r requirements.txt
```

#### Run tests

```
pytest
```

#### Run code against provided web service urls:

```
python app.py
```

#### How this can be extended

- all debts, payment plans and payments are stored in memory, this may not scale for huge amount of data, streaming json processing and/or storing the downloaded data in a local database (e.g. sqlite) may mitigate scale issues.
- the code internally uses Python's `datetime.datetime` type, it may or may not feasible to switch to the `datetime.date` type
- for the monetary data, it may or may not be feasible to find more appropriate Python package to use.
- the test cases are very basic, for the real production, more test cases would be added.
- next payment date is performed on the client, I would probably move that functionality to the service
