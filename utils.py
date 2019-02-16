def is_digit(number):
    if number.isdigit():
        return True

    try:
        int(number)
        return True
    except ValueError:
        return False