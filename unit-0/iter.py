def iter_slice(iList, step):
    if step < len(iList):
        tem = []
        i = 0                             #i 表示先在在第几步数
        if len(iList)%step == 0:
            no = len(iList)//step          #no 表示总的步数
        else:
            no = len(iList)//step + 1

        for x in iList:
            tem.append(x)
            if i == no-1:     #剩下的步数
                ttem = iList[i*step:]
                i+=1
                yield ttem
            else:
                if len(tem) % step == 0:
                    i += 1
                    if len(tem) == step:
                        ttem = tem
                    else:
                        ttem = tem[-step:]
                    yield ttem
    else:
        return "走的步数大于总的步数"

for x in iter_slice([1, 2, 3, 4, 5, 6,7,8], 6):
    print(x)

