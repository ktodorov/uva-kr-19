import time

timer1 = 0
timer2 = 0
timer3 = 0
timer4 = 0

def is_digit(number):
    if number.isdigit():
        return True

    try:
        int(number)
        return True
    except ValueError:
        return False

def contain_common_items(list1, list2):
    union_list = set(list1) & set(list2)

    return len(union_list) > 0

def measure_function(func):
    start = time.time()
    result = func()
    end = time.time()
    timer = (end - start)
    
    return (result, timer)