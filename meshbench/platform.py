"""Governance plane: scoped identity enforcement, A2A contract mediation and trace.

Boundaries are enforced by the database authorizer, not by the prompt. Every
table access by every principal is recorded whether it was allowed or denied.
"""
import sqlite3
import time

from .domains import ALL_TABLES, CONTRACTS, DOMAINS, derive_entitlements

_OK_ACTIONS = {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_FUNCTION, getattr(sqlite3, "SQLITE_RECURSIVE", 33)}


class Platform:
    def __init__(self, conn, model_name):
        self.conn = conn
        self.model_name = model_name
        self.principal = "admin"
        self.allowed = None          # None means unrestricted (platform admin only)
        self.accesses = []           # (principal, table, allowed)
        self.events = []             # structured trace
        self.a2a_tables = 0
        conn.set_authorizer(self._authorize)

    # ---- identity enforcement -------------------------------------------------
    def _authorize(self, action, arg1, arg2, dbname, source):
        if self.allowed is None:
            return sqlite3.SQLITE_OK
        if action == sqlite3.SQLITE_READ:
            ok = arg1 in self.allowed
            self.accesses.append((self.principal, arg1, ok))
            return sqlite3.SQLITE_OK if ok else sqlite3.SQLITE_DENY
        if action in _OK_ACTIONS:
            return sqlite3.SQLITE_OK
        self.accesses.append((self.principal, f"op:{action}", False))
        return sqlite3.SQLITE_DENY

    def run_as(self, principal, allowed, sql, max_rows=20):
        """Run a read-only query under a principal's entitlements."""
        self.principal, self.allowed = principal, set(allowed)
        before = len(self.accesses)
        try:
            cur = self.conn.execute(sql)
            cols = [c[0] for c in cur.description] if cur.description else []
            rows = cur.fetchmany(max_rows) if max_rows else cur.fetchall()
            result = {"ok": True, "columns": cols, "rows": rows}
        except sqlite3.Error as exc:
            denied = [t for (_, t, ok) in self.accesses[before:] if not ok]
            msg = (f"ACCESS DENIED: {', '.join(sorted(set(denied)))} is outside your charter"
                   if denied else f"SQL error: {exc}")
            result = {"ok": False, "error": msg}
        finally:
            self.principal, self.allowed = "admin", None
        self.log(principal, "sql", {"query": sql, "ok": result["ok"], "error": result.get("error")})
        return result

    def admin(self, sql, params=()):
        return self.conn.execute(sql, params)

    # ---- trace ----------------------------------------------------------------
    def log(self, principal, kind, payload):
        dom = DOMAINS.get(principal, {})
        self.events.append({
            "ts": time.time(), "principal": principal, "kind": kind, "payload": payload,
            "charter_version": dom.get("charter", {}).get("version"),
            "pack_version": dom.get("pack_version"), "model": self.model_name,
        })

    # ---- A2A contract check and result hand-over --------------------------------
    def check_contract(self, requester, provider, request_type):
        c = CONTRACTS.get(provider)
        if not c:
            return f"REFUSED: domain '{provider}' publishes no A2A contract"
        if requester not in c["requesters"]:
            return f"REFUSED: '{requester}' is not a contracted requester of '{provider}'"
        if request_type not in c["request_types"]:
            return f"REFUSED: request type '{request_type}' is not in the contract"
        return None

    def publish_ids(self, provider, sql):
        """Run the provider's query under the provider's identity and hand the ids to the requester."""
        res = self.run_as(provider, derive_entitlements(provider), sql, max_rows=0)
        if not res["ok"]:
            return None, res["error"]
        if len(res["columns"]) != 1:
            return None, "provider query must return exactly one id column"
        self.a2a_tables += 1
        name = f"a2a_result_{self.a2a_tables}"
        self.admin(f"CREATE TABLE {name}(id INTEGER)")
        self.conn.executemany(f"INSERT INTO {name} VALUES (?)", [(r[0],) for r in res["rows"]])
        return name, len(res["rows"])


def broad_entitlements():
    """The baseline: one credential that can read the whole estate."""
    return set(ALL_TABLES)
