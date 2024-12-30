def pr_four(str_list):
    for string in str_list:
        if len(string) == 4:
            print(string)

    return None

pr_four(["red", "rear","pink", "white", "green", "lime","aAa"])

def tup_sort(tup_list):
    sorted_dict = {}
    for tup in tup_list:
        sorted_dict[tup[1]] = tup[0]

    return sorted_dict

print(tup_sort([("a","x"),("b","y"),("c","z")]))

def closest_val(flo, int_list):
    closest_dist = abs(flo - int_list[0])
    closest_val = 0
    for integer in int_list:
        if abs(flo - integer) < closest_dist:
            closest_dist = abs(flo - integer)
            closest_val = integer
    return closest_val

print(closest_val(2.1, [1, 3, 4]))
