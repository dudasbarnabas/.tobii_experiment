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

while len(list) < 8:
    if first == "r" and second == "r":
        if rr < 2:
            rr += 1
            list.append(second)
            first = second
            second = random.choice(isi)
        else:
            second = random.choice(isi)
    elif first == "r" and second == "l":
        if rl < 2:
            rl += 1
            list.append(second)
            first = second
            second = random.choice(isi)
        else:
            second = random.choice(isi)
    elif first == "l" and second == "r":
        if rl < 2:
            rl += 1
            list.append(second)
            first = second
            second = random.choice(isi)
        else:
            second = random.choice(isi)
    elif first == "l" and second == "l":
        if rl < 2:
            rl += 1
            list.append(second)
            first = second
            second = random.choice(isi)
        else:
            second = random.choice(isi)
    print(list)
print()