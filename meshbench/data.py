"""Synthetic lender data: three bounded contexts in one SQLite database.

Everything is generated from a seed. No real customer data is used.
SSNs use the 900-999 area range, which is never issued.
"""
import random
import sqlite3

PRODUCTS = ["auto", "personal", "mortgage"]

SCHEMA = """
CREATE TABLE orig_applications(app_id INTEGER PRIMARY KEY, applicant_id INT, product TEXT,
  state TEXT, status TEXT, channel TEXT, uw_cd TEXT, amount REAL, submitted_date TEXT);
CREATE TABLE orig_applicants_pii(applicant_id INTEGER PRIMARY KEY, full_name TEXT, ssn TEXT, dob TEXT);
CREATE TABLE svc_loans(loan_id INTEGER PRIMARY KEY, app_id INT, product TEXT, principal REAL,
  balance REAL, status_cd TEXT, days_past_due INT, open_date TEXT);
CREATE TABLE svc_payments(payment_id INTEGER PRIMARY KEY, loan_id INT, amount REAL,
  paid_date TEXT, reversed INT);
CREATE TABLE svc_loan_notes(note_id INTEGER PRIMARY KEY, loan_id INT, note TEXT);
CREATE TABLE risk_accounts(loan_id INTEGER PRIMARY KEY, on_book INT, days_past_due INT,
  forbearance_flag INT, pd_score REAL, segment TEXT);
"""

NOTES = [
    "Customer requested hardship plan after job loss.",
    "Hardship review scheduled with collections.",
    "Customer called to confirm autopay date.",
    "Address change processed.",
    "Requested payoff quote.",
]


def _date(rng, year_lo=2021, year_hi=2025):
    return f"{rng.randint(year_lo, year_hi)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}"


def build(seed=7, n_applications=1500):
    """Return an in-memory connection holding the full synthetic estate."""
    rng = random.Random(seed)
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    loan_id = payment_id = note_id = 0
    for app_id in range(1, n_applications + 1):
        product = rng.choice(PRODUCTS)
        status = rng.choices(
            ["SUBMITTED", "IN_REVIEW", "APPROVED", "DECLINED", "WITHDRAWN", "FUNDED"],
            [5, 5, 5, 15, 10, 60])[0]
        amount = round(rng.uniform(3_000, 60_000) * (8 if product == "mortgage" else 1), 2)
        cur.execute("INSERT INTO orig_applications VALUES (?,?,?,?,?,?,?,?,?)",
                    (app_id, app_id, product, rng.choice(["IL", "TX", "CA", "NY", "OH"]), status,
                     rng.choice("DBP"), rng.choices(["S", "E", "M"], [80, 8, 12])[0], amount, _date(rng)))
        cur.execute("INSERT INTO orig_applicants_pii VALUES (?,?,?,?)",
                    (app_id, f"Applicant {app_id:05d}",
                     f"9{rng.randint(0, 99):02d}-{rng.randint(10, 99)}-{rng.randint(1000, 9999)}",
                     _date(rng, 1950, 2000)))
        if status != "FUNDED":
            continue
        loan_id += 1
        cd = rng.choices(["C", "D", "F", "X", "P"], [70, 12, 5, 5, 8])[0]
        dpd = {"C": rng.randint(0, 14), "D": rng.randint(15, 120), "F": rng.randint(0, 90),
               "X": rng.randint(121, 400), "P": 0}[cd]
        balance = 0.0 if cd == "P" else round(amount * rng.uniform(0.2, 0.98), 2)
        cur.execute("INSERT INTO svc_loans VALUES (?,?,?,?,?,?,?,?)",
                    (loan_id, app_id, product, amount, balance, cd, dpd, _date(rng)))
        cur.execute("INSERT INTO risk_accounts VALUES (?,?,?,?,?,?)",
                    (loan_id, 1 if cd in "CDF" else 0, dpd, 1 if cd == "F" else 0,
                     round(rng.random(), 4), rng.choices(["L1", "L2", "M1", "H1", "H2"], [30, 25, 25, 12, 8])[0]))
        for _ in range(rng.randint(0, 6)):
            payment_id += 1
            cur.execute("INSERT INTO svc_payments VALUES (?,?,?,?,?)",
                        (payment_id, loan_id, round(rng.uniform(100, 2500), 2), _date(rng),
                         1 if rng.random() < 0.08 else 0))
        if rng.random() < 0.2:
            note_id += 1
            cur.execute("INSERT INTO svc_loan_notes VALUES (?,?,?)", (note_id, loan_id, rng.choice(NOTES)))
    conn.commit()
    return conn


def clone(base):
    """Fresh private copy of the estate for one task run."""
    conn = sqlite3.connect(":memory:")
    base.backup(conn)
    return conn
