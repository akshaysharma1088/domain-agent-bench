"""Domain definitions: tables, charters, context packs and A2A contracts.

These are the domain-owned, versioned artifacts of the architecture.
"""

HOME = "servicing"
REGULATED = {"orig_applicants_pii"}

DOMAINS = {
    "servicing": {
        "tables": ["svc_loans", "svc_payments", "svc_loan_notes"],
        "charter": {
            "version": "1.0", "tier": "T0",
            "objectives": ["Answer servicing portfolio questions with a single query"],
            "permitted": ["read:svc_loans", "read:svc_payments", "read:svc_loan_notes"],
            "exclusions": ["regulated data classes", "tables owned by other domains"],
            "budget": {"max_steps": 8, "max_a2a": 3},
        },
        "pack_version": "1.0",
        "pack": (
            "Servicing glossary. status_cd codes: C=current, D=delinquent, F=forbearance, "
            "X=charged off, P=paid off. An ACTIVE LOAN in Servicing is any loan still on the books: "
            "status_cd in (C, D, F). DELINQUENT means status_cd = D. A PAYMENT RECEIVED excludes "
            "reversed payments (reversed = 1). svc_loans.app_id is the key of the originating application."
        ),
    },
    "originations": {
        "tables": ["orig_applications", "orig_applicants_pii"],
        "charter": {
            "version": "1.0", "tier": "T0",
            "objectives": ["Interpret application data for contracted requesters"],
            "permitted": ["read:orig_applications"],
            "exclusions": ["regulated data classes"],
            "budget": {"max_steps": 1, "max_a2a": 0},
        },
        "pack_version": "1.0",
        "pack": (
            "Originations glossary. channel codes: D=direct, B=broker, P=partner. uw_cd codes: "
            "S=standard approval, E=approved by exception, M=manual review. An ACTIVE APPLICATION is "
            "one still in progress: status in (SUBMITTED, IN_REVIEW, APPROVED). FUNDED applications "
            "became loans. orig_applicants_pii is a regulated table and is never shared."
        ),
    },
    "risk": {
        "tables": ["risk_accounts"],
        "charter": {
            "version": "1.0", "tier": "T0",
            "objectives": ["Interpret risk account data for contracted requesters"],
            "permitted": ["read:risk_accounts"],
            "exclusions": [],
            "budget": {"max_steps": 1, "max_a2a": 0},
        },
        "pack_version": "1.0",
        "pack": (
            "Risk Analytics glossary. An ACTIVE ACCOUNT in Risk is on the books (on_book = 1), not in "
            "forbearance (forbearance_flag = 0) and less than 30 days past due. This is narrower than "
            "the Servicing meaning of active. segment codes: L1, L2 = low; M1 = medium; H1, H2 = HIGH "
            "risk. risk_accounts.loan_id is the servicing loan key."
        ),
    },
}

# Agent-to-agent contracts, published by the providing domain.
CONTRACTS = {
    "originations": {"version": "1.0", "requesters": ["servicing"],
                     "request_types": ["select_ids", "explain"], "key": "app_id",
                     "terms": "Returned ids may be joined to svc_loans.app_id. No applicant attributes are returned."},
    "risk": {"version": "1.0", "requesters": ["servicing"],
             "request_types": ["select_ids", "explain"], "key": "loan_id",
             "terms": "Returned ids may be joined to svc_loans.loan_id."},
}

ALL_TABLES = [t for d in DOMAINS.values() for t in d["tables"]]


def owner_of(table):
    for name, d in DOMAINS.items():
        if table in d["tables"]:
            return name
    return None


def derive_entitlements(domain):
    """Scoped identity: entitlements are derived mechanically from the charter."""
    return {p.split(":", 1)[1] for p in DOMAINS[domain]["charter"]["permitted"] if p.startswith("read:")}
