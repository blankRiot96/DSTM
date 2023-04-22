def int_to_commas(num: int) -> str:
    """130123 -> 130,123"""

    num_seq = str(num)
    comma_num = ""
    for i, e in enumerate(num_seq):
        i += 1
        if i % 3 == 0:
            comma_num += ","
        comma_num += e

    return comma_num


print(format(12_391_912, ","))
print(format(12_391_912, ","))

print(format(12_391_912, ","))

print(format(1300, ","))
