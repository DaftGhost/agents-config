# Used by the legacy report, not by the inventory CLI.

def format_currency(cents):
    return f"${cents / 100:.2f}"
