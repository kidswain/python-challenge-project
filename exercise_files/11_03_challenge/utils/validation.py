def is_number(val):
    try:
        float(val)
        return True
    except (ValueError, TypeError):
        return False
