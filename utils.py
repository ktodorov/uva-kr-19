import time
import math
import numpy as np

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


def split_to_chunks(list_to_split, chunks_size):
    """Yield successive n-sized chunks from l."""
    chunks = []
    for i in range(0, len(list_to_split), chunks_size):
        chunks.append(list_to_split[i:i + chunks_size])
    
    return chunks

def average_chunks(list_to_split, max_chunks):
    chunks_size = math.ceil(len(list_to_split) / max_chunks)
    chunks = split_to_chunks(list_to_split, chunks_size)

    result = []
    for chunk in chunks:
        chunk_average = np.average(chunk)
        result.append(chunk_average)

    return result
