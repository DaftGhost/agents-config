from db import query


def quarterly_report(quarter):
    # Compliance report: counts logins per quarter, including years before auth_events existed
    return query("SELECT COUNT(*) FROM login_history WHERE quarter = ?", quarter)
