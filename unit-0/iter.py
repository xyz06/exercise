def iter_slice(List, step):
    ltg = len(List)
    no = 0
    i = 0
    while no < ltg:
        tem = List[no:(i + 1) * step]
        yield tem
        i += 1
        no += step

for x in iter_slice([1, 2, 3, 4, 5, 6, 7, 8], ):
    print(x)
