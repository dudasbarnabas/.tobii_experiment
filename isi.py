import random

blokk = []
isi = ["r", "l"]

rr = 0
rl = 0
lr = 0
ll = 0

list = []
first = random.choice(isi)
list.append(first)
blokk.append(first)
second = random.choice(isi)

out = 8
max_pair = 2

while len(list) < out:
    while list.count("r") < (out/2) and list.count("l") < out/2:
        if first == "r" and second == "r":
            if rr < max_pair:
                rr += 1
                list.append(second)
                first = second
                second = random.choice(isi)
            else:
                second = random.choice(isi)
        elif first == "r" and second == "l":
            if rl < max_pair:
                rl += 1
                list.append(second)
                first = second
                second = random.choice(isi)
            else:
                second = random.choice(isi)
        elif first == "l" and second == "r":
            if lr < max_pair:
                lr += 1
                list.append(second)
                first = second
                second = random.choice(isi)
            else:
                second = random.choice(isi)
        elif first == "l" and second == "l":
            if ll < max_pair:
                ll += 1
                list.append(second)
                first = second
                second = random.choice(isi)
            else:
                second = random.choice(isi)
    else:
        if list.count("r") == (out/2):
            for i in range(out - len(list)):
                list.append("l")
        elif list.count("l") == (out/2):
            for i in range(out - len(list)):
                list.append("r")
    print(list)
print()


rr = rl = lr = ll = 0

# go through consecutive pairs
for a, b in zip(list, list[1:]):
    if a == "r" and b == "r":
        rr += 1
    elif a == "r" and b == "l":
        rl += 1
    elif a == "l" and b == "r":
        lr += 1
    elif a == "l" and b == "l":
        ll += 1

print(rr, rl, lr, ll)


for k in range(10):
    sum_num = []
    final = []
    for i in range(4):
        sum_num.append(round(random.uniform(2,6),1))
        sum_num.append(round(random.uniform(6,10),1))
    plusmin = round(((48-(sum(sum_num)))/8),1)
    resid = 48-(sum(sum_num))
    plusmin = divmod((resid*10),8)[0]/10
    
    for i in sum_num:
        rounded = round((i+plusmin),1)
        final.append(rounded)
    rest = round(48-sum(final),1)
    order = sorted(sum_num)
    order[0] = order[0]+rest
    print(final)
    print(sum(final))
    print(sum(final)+rest)


