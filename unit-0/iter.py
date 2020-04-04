def iter_slice(iList, step):
    ltg = len(iList)
    no = 0
    while no < ltg:
        yield iList[no:(no // 2 + 1) * step]
        no += step



for x in iter_slice([1, 2, 3, 4, 5, 6], ):
    print(x)