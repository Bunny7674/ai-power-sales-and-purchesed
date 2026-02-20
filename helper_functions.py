def format_currency(x):
    try:
        return f"${x:,.2f}"
    except Exception:
        return str(x)
