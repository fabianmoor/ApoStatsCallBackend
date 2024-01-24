def is_sum_greater(data):
    return sum(data.values())



all_calls = {
    "JULIA": 4,
    "MILLA": 6,
    "VALDEMAR": 6,
    "SOFIA": 2,
    "FABIAN": 5,
}

print(is_sum_greater(all_calls))
